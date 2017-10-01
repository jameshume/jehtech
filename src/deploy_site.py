from __future__ import division
import os
import zlib
import pickle
import string 
import path_record
import traceback
import sys
if sys.version_info[0] < 3:
	import ftplib_mod as ftplib
else:
	import ftplib_mod_py3 as ftplib

DB_FILENAME = 'deployment_db.bin'
DEPLOYED_DIR = os.path.join('..','__deployed')
FTP_ADDRESS="000kwjq.wcomhost.com"
FTP_USER_ID="ftp3286307"

def GenerateCheckSum(data):
	return zlib.adler32(data) & 0xffffffff

def istext(filename):
	base = os.path.basename(filename)
	print("BASE='{}'".format(base))
	dotIdx = base.rfind(".")
	ext = base[dotIdx+1:].strip().lower()
	print("EXT='{}'".format(ext))
	print("TEXT? = {}".format(ext in ['html', 'htm', 'txt', 'ipynb', 'js', 'css']))
	return ext in ['html', 'htm', 'txt', 'ipynb']

fileCRC = {}
newFiles     = []
removedFiles = []
commonFiles  = []

# Get the CRC of every file under the __deployed directory so we can figure out which
# files have changed... Save the CRC in a dictionary with a key that is the full path to the file relative to
# the CWD
print("Building CRC map of {}... ".format(DEPLOYED_DIR))
for dirpath, dirnames, filenames in os.walk(DEPLOYED_DIR):
	for filename in filenames:
		fullPath = os.path.join(dirpath, filename)
		with open(fullPath, 'rb') as fh:
			fileCRC[fullPath] = GenerateCheckSum(fh.read())
print("Done\n")

if os.path.isfile(DB_FILENAME):
	# use the existing database to find out which files are new since the last upload, which
	# have been deleted and which are just modified so only these are copied...
	# The DB is just a dictionary with a key that is the full path to the file relative to
   # the CWD
	prevFileCRC  = pickle.load(open(DB_FILENAME, 'rb'))
	prevFiles    = set(prevFileCRC.keys())
	nowFiles     = set(fileCRC.keys())
	newFiles     = nowFiles.difference(prevFiles)
	removedFiles = prevFiles.difference(nowFiles)
	commonFiles  = prevFiles.intersection(nowFiles)

	#
	# Out of the common files, only keep the files that have not changed between the DB record
	# of the last deploy and the current file
	unchanged = set()
	for filename in commonFiles:
		if prevFileCRC[filename] == fileCRC[filename]:
			unchanged.add(filename)
	commonFiles.difference_update(unchanged)
else:
	# There is no existing database. Assume that the HTML folder is empty so therefore
	# all files are new..
	print("The database file {} does not exist\n".format(DB_FILENAME))
	newFiles = fileCRC.keys()
	print(fileCRC)


print("\nThe following files have changed")
print(commonFiles)

print("\nThe following files have been removed")
print(removedFiles)

print("\nThe following files have been added")
print(newFiles)

print("\nAttempting to FTP into server")

def ConvertPcLocalToHostLocal(filename):
	# drop the __depolyed front. then need to figure out whether the directory tree exists. if it does copy, otherwise create directory tree and then copy!
	return os.path.split(filename)[1] 


class MyFTP(object):
	""" Mostly to put random files. the ftplib functions don't appear to do things 
	    like recursive directory creation and also to avoid having to do continual
		 directory listings from the server and therefore save a little upload time
		 I am going to cache directories seen and made so far on mass uploads """

	def __init__(self, ftp):
		self._pr = path_record.PathRecord() # All paths must be absolute
		self._ftp = ftp                     # FTPLib object

	def mkd_recursive(self, path):
		if type(path) == str:
			path = self._pr.pathExplode(path)
		
		if len(path) < 1:
			return

		# found is boolean, yes/no
		# partial is longest list of common path elements seen so far in cache
		found, partial = self._pr.havePath(path)
		if found:
			return

		saveDir = self._ftp.pwd()
		try:
			partialLen = len(partial)
			if partialLen > 0:
				self._ftp.cwd('/' + '/'.join(partial))
	
			
			for pathEl in path[partialLen:]:
				self._ftp.mkd(pathEl)
				self._ftp.cwd(pathEl)
		finally:
			self._ftp.cwd(saveDir)

	def putFile(self, localFilename):
		# need to figure out if the directory exists and if not create it and any parent
		# directories necessary
		dirChanged = False
		saveDir = self._ftp.pwd()
		print("PUTTING file {}".format(localFilename))
		print("   Current FTP dir = {}".format(saveDir))
		print("   Searching for common prefix between")
		print("      - {}".format(DEPLOYED_DIR))
		print("      - {}".format(localFilename))

		commonPrefix = self._pr.pathExplode(os.path.commonprefix([DEPLOYED_DIR, localFilename]))
		pathElements = self._pr.pathExplode(localFilename)[len(commonPrefix):] # drop the DEPOLYED DIR path prefix
		dirElements  = pathElements[:-1]

		print("   commonPrefix = {}".format(commonPrefix))
		print("   pathElements = {}".format(pathElements))
		print("   dirElements  = {}".format(dirElements))
		if len(dirElements) > 0:
			print("   Saved dir is {}".format(saveDir))
			found, partial = self._pr.havePath(dirElements)
			print("   found = {}".format(found))
			print("   partial = {}".format(partial))
			partial = self._pr.pathExplode(partial)
			print("   Found in cache = {}".format(found))
			print("   Partial found '{}'".format(partial))
			if not found:
				print("   Directory '{}' not found in cache".format(dirElements))
				print("   The partial '{}' was found in cache".format(partial))
				partialLen = len(partial)
				pathDiverged = False
				for idx, pathEl in enumerate(dirElements):
					pathDiverged = pathDiverged or ((idx >= partialLen) or (pathEl != partial[idx]))
					if pathDiverged:
						print("   Current pathEl is {}, past partial at idx {}".format(pathEl, idx))
						print("   Joining list {}".format(dirElements[0:idx]))
						dirToList = '/'.join(dirElements[0:idx])
						print("   Getting listing of {}".format(dirToList))
						print("   CWD is {}".format(self._ftp.pwd()))
						dirList = self._ftp.nlst(dirToList)
						lastDirInList = [x.split("/")[-1] for x in dirList]
						print("   DirList IS {}".format(dirList))
						print("   LastDirInList is {}".format(lastDirInList))
						print("   Searching for {} in dirlist".format(dirElements[idx]))
						if dirElements[idx] not in lastDirInList:
							# The mkd() function can not create directories
							print("      Creating {}".format(os.path.join(*dirElements[0:idx+1])))
							if idx > 0:
								print("      CWD is {}".format(self._ftp.pwd()))
								print("      Changing to {}".format(os.path.join(*dirElements[0:idx])))
								self._ftp.cwd("/".join(dirElements[0:idx]))
								dirChanged = True
								print("      CWD is {}".format(self._ftp.pwd()))
							print("      Making {}".format(dirElements[idx]))
							self._ftp.mkd(dirElements[idx])
						else:
							print("      Directory {} already exists on server".format(dirElements[idx]))
				print("   Storing path to cache")
				self._pr.addPath(dirElements)
			if dirChanged:
				print("Restoring saved dir {}".format(saveDir))
				self._ftp.cwd(saveDir)
	
		saveDir = None
		if len(dirElements) > 0:
			targetDir = "/".join(dirElements)
			saveDir = self._ftp.pwd()
			self._ftp.cwd(targetDir)
		else:
			targetDir = "."
	
		if istext(localFilename):
			print('   STOR TEXT {} to dir {} from {} as {}'.format(pathElements[-1], targetDir, localFilename, 'ascii'))
			print('   - STOR {}'.format(pathElements[-1]))
			# For some reason in Python 3 the FTP library needs to read back bytes
			# not str but doesn't seem to be for all files... didnt bother to get
			# to the bottom of this! 
			self._ftp.storlines('STOR {}'.format(pathElements[-1]), open(localFilename, 'rb'))
		else:
			print('   STOR BIN {} to dir {} from {} as {}'.format(pathElements[-1], targetDir, localFilename, 'binary'))
			self._ftp.storbinary('STOR {}'.format(pathElements[-1]), open(localFilename, 'rb'))

		if len(dirElements) > 0:
			self._ftp.cwd(saveDir)

ftpWasSuccessfull = True
ftp = None
try:
	ftp = ftplib.FTP(FTP_ADDRESS, FTP_USER_ID, sys.argv[1]) 
	ftp.set_debuglevel(0)

	myftp = MyFTP(ftp)

	#dirlist = ftp.nlst()
	#if 'html' not in dirlist:
	#	ftp.mkd('html')
	
	ftp.cwd('htdocs')
	
	for filename in newFiles:
		assert(os.path.isfile(filename))
		myftp.putFile(filename)

	for filename in commonFiles:
		assert(os.path.isfile(filename))
		myftp.putFile(filename)

	for filename in removedFiles:
		assert(not os.path.isfile(filename))
		destFilename = ConvertPcLocalToHostLocal(filename)
		print("deleting {}".format(destFilename))
		try:
			ftp.delete(destFilename)
		except:
			print("### IFNORING DELETE ERROR")


except Exception as e:
	print(e)
	print(traceback.format_exc())
	ftpWasSuccessfull = False
finally:
	if ftp is not None:
		ftp.quit()

if ftpWasSuccessfull:
	print("\nSaving new deployment database")
	pickle.dump(fileCRC, open(DB_FILENAME, 'wb'))
else:
	print("\nThe FTP failed so NOT saving database")




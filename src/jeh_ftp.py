import ftplib
import path_record

class JehFTP(object):
	""" Mostly to put random files. the ftplib functions don't appear to do things 
	    like recursive directory creation and also to avoid having to do continual
		 directory listings from the server and therefore save a little upload time
		 I am going to cache directories seen and made so far on mass uploads """

	def __init__(self, ftp):
		self._pr  = path_record.PathRecord() # All paths must be absolute
		self._ftp = ftp                      # FTPLib object
		self._cwd = '/'                      # Must always be an absolute path

	def cwd(self, path):
		""" Change current working directory but remember where we are so we dont
		    have to do a remote query. Path may be relative or absolute. Path must
			 be a string. """
		path = path.strip()
		self._ftp.cwd(path)
		if path[0] == '/': self._cwd = path
		else:              self._cwd += '/' + path
		assert(path[0] == '/' or path[0] != '\\')

	def mkd_recursive(self, path):
		""" Recursively make a directory. Path must be a string, can be 
		    relative or absolute """
		path = path.strip()
		if len(path) < 1:
			return

		# if path is relative convert it to absolute...
		if path[0] != '/' and path[0] != '\\':
			path = self._cwd + '/' + path

		# found is boolean, yes/no
		# partial is longest list of common path elements seen so far in cache
		pathEls = self._pr.pathExplode(path)
		found, partial = self._pr.havePath(pathEls)
		if found:
			return
		
		# Recursively create the directory but saving the current directory so
		# we can restore it after we're done creating...
		saveDir = self._cwd
		try:
			partialLen = len(partial)
			if partialLen > 0:
				self._ftp.cwd('/'.join(partial))
			
			for pathEl in pathEls[partialLen:]:
				self._ftp.mkd(pathEl)
				self.cwd(pathEl)

			self._pr.addPath(path)
		finally:
			self._ftp.cwd(saveDir)


if __name__ == "__main__":
	password = raw_input('Enter password: ')
	ftp = ftplib.FTP('ftp.jeh-tech.com', 'jhume', password) 
	ftp.set_debuglevel(2)

	jftp = JehFTP(ftp)
	jftp.mkd_recursive("/aaa/bbb/ccc/ddd")


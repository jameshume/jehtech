class JehFTP(object):
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
		
		# Recursively create the directory but saving the current directory so
		# we can restore it after we're done creating...
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


if __name__ == "__main__":

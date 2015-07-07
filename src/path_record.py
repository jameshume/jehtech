import os

class PathRecord:
	"""Acts as a cache of paths that have already been seen. Basically builds up a client side
	   map of a directory tree, directories only"""

	def __init__(self):
		# Paths is a dictionary with directory name mapping to a dictionary giving
		# directory names under that directory.
		self._paths = {} 
	
	def pathExplode(self, path):
		""" Explode a path string into a list with each list element
		    being a path component. If the path is absolute make sure to record
			 the first seperator. """
		if len(path) == 0:
			return []

		l = []
		head, tail = os.path.split(os.path.normpath(path))
		if (len(head) < 1) and (len(tail) < 1): # If path is empty, both head and tail are empty
			return l
		
		if len(tail) < 1: # If path ends in a slash, tail will be empty
			head, tail = os.path.split(head)
		
		while len(tail) > 0:
			l.insert(0, tail)
			head, tail = os.path.split(head)
		
		if path[0] == '/' or path[0] =='\\':
			l.insert(0, path[0])

		return l

	def havePath(self, path):
		"""Returns (True, commonPath) if the path is in our records, (False, commonPath) otherwise
		   where commonPath is the same as path if True was returned, otherwise it is the deepest
			path seen that matches as much of path as possible"""
		print "Searching for path {}".format(path)
		pathEls = None
		if type(path) == str:
			pathEls = self.pathExplode(path)
		else:
			if any([type(x)!=str for x in path]):
				raise Exception("PathRecord: If path is array it must be an array of strings")
			pathEls = path

		pathExists = True
		currDirDict = self._paths
		pathSoFar = ""
		for pathEl in pathEls:
			if pathEl not in currDirDict:
				pathExists = False
				break
			pathSoFar = os.path.join(pathSoFar, pathEl)
			currDirDict = currDirDict[pathEl]
		
		return (pathExists, pathSoFar)

	def addPath(self, path):
		""""Adds a path to the record of paths seen"""
		pathEls = None
		if type(path) == str:
			pathEls = self.pathExplode(path)
		else:
			if any([type(x)!=str for x in path]):
				raise Exception("PathRecord: If path is array it must be an array of strings")
			pathEls = path
		
		currDirDict = self._paths
		for pathEl in pathEls:
			if pathEl not in currDirDict:
				currDirDict[pathEl] = {}
			currDirDict = currDirDict[pathEl]


if __name__ == "__main__":
	pr = PathRecord()
	pathEls = ["aa", "bb", "cc", "dd"]
	pr.addPath(os.path.join(*pathEls))

	# Can detect all elements in the path
	detectPath = pathEls[0]
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	detectPath = os.path.join(*pathEls[0:2])
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	detectPath = os.path.join(*pathEls[0:3])
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	detectPath = os.path.join(*pathEls[0:4])
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	# Can detect a path we don't have
	detectPath = "bb"
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(not found)
	assert(commonPath == "")

	# Can detect a part of a path that we partially have
	newPathEls = pathEls[0:2]
	newPathEls.extend(["ee"])
	detectPath = os.path.join(*newPathEls)
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(not found)
	assert(commonPath == os.path.join(*pathEls[0:2]))

	# Add another branch to an existing directory and make sure we get it
	pathEls2 = ["aa", "qq", "ww"]
	pr.addPath(os.path.join(*pathEls2))

	detectPath = pathEls2[0]
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	detectPath = os.path.join(*pathEls2[0:2])
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	detectPath = os.path.join(*pathEls2[0:3])
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == detectPath)

	# Make sure we can find paths using arrays and not strings
	detectPath = pathEls2[0:2]
	found, commonPath = pr.havePath(detectPath)
	print found, commonPath
	assert(found)
	assert(commonPath == os.path.join(*detectPath[0:2]))



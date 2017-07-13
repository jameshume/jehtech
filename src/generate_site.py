"""
Assume the dir structure has
	+ html:       contains all HTML files for the site
	+ images:     contains all images for the site
	+ javascript: contains all javascript used by the site. seperate files
	              that will be combiend into one file and minimised. The order
	              of inclusion into the monolith is defined in order.txt
	+ css:        contains all CSS used by the site. seperate files that
	              will be combined intil one file and minimised. The order
	              of inclusion into the monolith is defined in order.txt

Script will delete the directory "__deployed" and will re-create it with the
site contents. html dir is collapsed into this dir and the css and javascript files
are too.
"""
import os
import fnmatch
import re
import shutil
import lxml.html
import lxml.etree
import sys
import errno
import subprocess
import zlib
import shutil
import pickle
import codecs
import pathlib

DEPLOYED_DIR = '../__deployed'

def GenerateRunningCheckSum(data, value):
	return zlib.adler32(data, value) & 0xffffffff

def combine_files(base_dir, dest_file, is_debug=False):
	print("COMBINING", base_dir, dest_file)
	un_minimised_temp_aggregate_file = os.path.join(base_dir, "un_minimised_temp_aggregate.file")
	minimised_aggregate_file = os.path.join(base_dir, "minimised_aggregate.file")
	indexFileName     = os.path.join(base_dir, "contents.txt")
	indexInfoFilename = os.path.join(base_dir, "contents.data")

	#
	# Do a running CRC of all the files listed in the index
	runningCRC = 0
	with open(indexFileName, 'r') as idxFh:
		for filename in idxFh.readlines():
			with open(os.path.join(base_dir, filename.strip()), 'rb') as fh:
				runningCRC = GenerateRunningCheckSum(fh.read(), runningCRC)

	foundPrevRunningCRC = False
	prevRunningCRC = 0
	if os.path.isfile(indexInfoFilename):
		print("Loading {}".format(indexInfoFilename))
		prevRunningCRC = pickle.load(open(indexInfoFilename, 'rb'))
		foundPrevRunningCRC = True

	# Only regenerate the unminimsed combination of all the JS files if need be
	regenerated = False
	if os.path.isfile(un_minimised_temp_aggregate_file) and foundPrevRunningCRC and (prevRunningCRC == runningCRC):
		print('The contents of "{}" has not changed. Skipping regeneration step.'.format(base_dir))
	else:
		print('The contents of "{}" has changed. Regenerating...'.format(base_dir))
		regenerated = True
		pickle.dump(runningCRC, open(indexInfoFilename, 'wb'))
		fh     = open(indexFileName, 'r')
		fh_new = open(un_minimised_temp_aggregate_file, 'w')
		for filename in fh.readlines():
			filename = filename.strip()
			print("\t", filename)
			fh_curr = open(os.path.join(base_dir, filename), 'r')
			fh_new.write(fh_curr.read())
			fh_curr.close()
		fh_new.close()
		fh.close()

	if is_debug:
		print("### NOTE: This is a debug run so minimised file is just a copy of unmin")
		shutil.copyfile(un_minimised_temp_aggregate_file, minimised_aggregate_file)
	elif regenerated or not os.path.isfile(minimised_aggregate_file):
		print("Calling yuicompressor...")
		fileType="js"
		if dest_file[-3:] == "css": fileType="css"
		args = ["java", "-jar",  "yuicompressor-2.4.8.jar",  "--type", fileType, "-o", minimised_aggregate_file, un_minimised_temp_aggregate_file]
		print(args)
		subprocess.call(args)

	print("Copying {} to {}".format(minimised_aggregate_file, dest_file))
	shutil.copyfile(minimised_aggregate_file, dest_file)


def mkdir_p(path):
	""" Recursively make a directory path """
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def find_html_files(base_dir):
	""" Generator, find all HTML files recursively in base dir but does not
	    recurse into directories starting with an underscore and ignores all
	    files starting with an underscore """
	for dirname, directories, filenames in os.walk(base_dir):
		# Must remove IN PLACE for os.walk to skip these directories
		i = 0
		while i < len(directories):
			if directories[i][0] == '_':
				del directories[i]
			else:
				i = i + 1

		# Must remove IN PLACE for os.walk to skip these files
		i = 0
		while i < len(filenames):
			if filenames[i][0] == '_':
				del filenames[i]
			else:
				i = i + 1

		for filename in fnmatch.filter(filenames, '*.html'):
			yield (dirname, filename)
		for filename in fnmatch.filter(filenames, '*.php'):
			yield (dirname, filename)
		for filename in fnmatch.filter(filenames, '*.js'):
			yield (dirname, filename)

def path_explode(path):
	""" Explode a path string into a list with each list element
	    being a path component """
	l = []
	head, tail = os.path.split(os.path.normpath(path))
	if (len(head) < 1) and (len(tail) < 1): # If path is empty, both head and tail are empty
		return l

	if len(tail) < 1: # If path ends in a slash, tail will be empty
		head, tail = os.path.split(head)

	while len(tail) > 0:
		l.insert(0, tail)
		head, tail = os.path.split(head)

	return l

def get_relative_to_root(currentDirName):
	dirSplit = path_explode(currentDirName)
	newLink = ""
	if (len(dirSplit) > 0) and (dirSplit[0] != '.'):
		newLink = '/'.join([r'..' for x in range(len(dirSplit))])
	return newLink

def get_links_insert(currentDirName):
	""" Read in the links HTML and modify the links so that they work from the
	    directory of the current web page """
	doc = lxml.html.parse('_links.html')
	newLink = get_relative_to_root(currentDirName)
	if newLink != "":
		# We're no longer in the base directory. All links must now be made relative
		# to this new directory...
		for el, at, link, pos in doc.getroot().iterlinks():
			if (el.tag == 'a') and (at == 'href'):
				el.set(at, newLink + '/' + el.get(at))

	linksHtml = lxml.etree.tostring(doc.getroot().get_element_by_id("jehtech_contents_div"), pretty_print=True, method='html').decode()
	return linksHtml

def create_references(contents):
	"""
	## REF LIST START ##
	##Short name@long descr@link##
	## REF LIST END ##
	"""
	start_refs = re.compile(r'^\w*##\w*REF\w+LIST\w*START\w*##')
	end_refs = re.compile(r'^\w*##\w*REF\w+LIST\w+END\w*##')
	a_ref = re.compile(r'^\w*##\w*([^@]+)\w*@\w*([^@]+)\w*@\w*([^@]+)##')

	start_found = False
	end_found = False
	for lineno, line in enumerate(contents):
	    line = line.strip()
	    if start_refs.match(line) is not None:
	        conents[lineno] = "<ol>"
	        start_found = True
	        break

	if not start_found:
	    print("No reference section found")
	    return

	for line in in_fh:
	    line = line.strip()

	    if end_refs.match(line) is not None:
	        conents[lineno] = "<\ol>"
	        end_found = True
	        break

	    m = a_ref.match(line)
	    if m is not None:
	        if end_found:
	            raise Exception("Reference spec found after reference section end")
	        contents[lineno] = """<li><a name="{}" href="{}" target="_blank">{}</a>.
	   </li>
	""".format(m.group(0), m.group(2), m.group(1))

	if not end_found:
	    raise Exception("Could not find end of reference section")

def deploy_site():
	# Delete any existing deployment and begin creating a new one...
	if os.path.isdir(DEPLOYED_DIR):
		shutil.rmtree(DEPLOYED_DIR)
	os.mkdir(DEPLOYED_DIR)

	# Combine javascript and CSS files into monoliths
	monoJsFilename  = os.path.join(DEPLOYED_DIR, 'jeh-monolith.js')
	combine_files("./javascript", monoJsFilename)

	monoCssFilename = os.path.join(DEPLOYED_DIR, 'jeh-monolith.css')
	combine_files("./css", monoCssFilename)

	# Regex to put in the links into all the HTML pages
	prog = re.compile('(<\s*div\s+id\s*=\s*"includedContent"\s*>)', re.IGNORECASE)

	# Regexs to put in JS and CSS
	prog_css = re.compile('(<!--\s*CSS_INSERT\s*-->)', re.IGNORECASE)
	prog_js  = re.compile('(<!--\s*JAVASCRIPT_INSERT\s*-->)', re.IGNORECASE)
	prog_img = re.compile('##IMG_DIR##')

	last_dirname = None
	link_to_root = ""
	doc = None
	os.chdir('html')
	sitemap_list = []
	for dirname, filename in find_html_files('.'):
		# If we have changed directory we must regenerate the links page so that the
		# links are relative to this new directory
		if dirname != last_dirname:
			link_to_root = get_relative_to_root(dirname)
			linksHtml = get_links_insert(dirname)
			last_dirname = dirname

		# Read in the current HTML files contents
		htmlFileName = os.path.join(dirname, filename)
		print("Deploying", dirname, filename, htmlFileName)


		if fnmatch.fnmatch(filename, '*.html'):
			## dirty hackery
			dirs = list(os.path.split(dirname))
			if len(dirs) > 1:
				if dirs[0] == ".":
					dirs = dirs[1:]

			dirs.append(filename)
			google_sitemap_ref = "http://www.jeh-tech.com/{}".format(pathlib.PurePosixPath(*dirs))
			sitemap_list.append(google_sitemap_ref)

		htmlFile = codecs.open(htmlFileName, 'r', 'utf-8')
		#htmlFile = open(htmlFileName, 'r')
		htmlFileContents = htmlFile.read();
		htmlFile.close()

		# Create and open the file in the deployed folder.
		deployed_dir = os.path.join('..', DEPLOYED_DIR, dirname)
		if (dirname != '.'):
			if not os.path.exists(deployed_dir):
				print("Creating directory {}".format(deployed_dir))
				mkdir_p(deployed_dir)
			newFileName = os.path.join('..', DEPLOYED_DIR, dirname, filename)
			print("(A) Opening new file {}".format(newFileName))
		else:
			newFileName = os.path.join('..', DEPLOYED_DIR, filename)
			print("(B) Opening new file {}".format(newFileName))

		# Copy the contents of the curr html to it's deployed file but add in the
		# links page
		htmlFileContents = prog.sub(r'\1' + linksHtml, htmlFileContents)
		htmlFileContents = prog_css.sub('<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" />'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
		htmlFileContents = prog_js.sub('<script src="{}{}jeh-monolith.js"></script>'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
		htmlFileContents = prog_img.sub('{}{}images/jeh-tech'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
		#newFile = open(newFileName, 'w')
		newFile = codecs.open(newFileName, 'w', 'utf-8')
		newFile.write(htmlFileContents)
		newFile.close()
	os.chdir('..')

	#
	# Write out google sitemap as a basic utf-8 text file
	with codecs.open(os.path.join(DEPLOYED_DIR, "sitemap.txt"), "w", "utf-8") as sitemap_file:
		sitemap_file.writelines("%s\n" % line for line in sitemap_list)

	#
	# Now copy across all other important files
	nonHtmlFiles = [ #'reCaptchaSecret.txt',
	                 'robots.txt',
	                 'downloadables',
	                 'images',
	                 'fonts']

	for filename in nonHtmlFiles:
		if os.path.exists(filename):
			target = os.path.join(DEPLOYED_DIR, filename)
			if os.path.isdir(filename):
				print("Copying directory", filename, "to", target)
				shutil.copytree(filename, target)
			elif os.path.isfile(filename):
				print("Copying file", filename, "to", target)
				shutil.copy(filename, target)
			else:
				raise Exception('### WARNING: {} not copied!'.format(filename))
		else:
			raise Exception('### WARNING: {} does not exist!'.format(filename))

try:
	deploy_site()
except:
	#if os.path.isdir(DEPLOYED_DIR):
	#	shutil.rmtree(DEPLOYED_DIR)
	raise
	pass

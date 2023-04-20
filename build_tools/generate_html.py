import sys
import os
import re
import subprocess
import codecs
import platform
import shutil

SRC_FILE = sys.argv[1]
DST_FILE = sys.argv[2]
ROOT_DIR = sys.argv[3]

print("Generating {} from {}".format(DST_FILE, SRC_FILE))

def get_links_insert(currentDirName):
	return ""

# Regex to put in the links into all the HTML pages
prog_add_links_to_page = re.compile('(<\s*div\s+id\s*=\s*"includedContent"\s*>)', re.IGNORECASE)
# Regexs to put in JS and CSS
prog_css = re.compile('(<!--\s*CSS_INSERT\s*-->)', re.IGNORECASE)


# Open and read in the source file
htmlFileContents = ""
with codecs.open(SRC_FILE, 'r', 'utf-8') as htmlFile:
	htmlFileContents = htmlFile.read();


# Open and read in the links file
linksHtml = ""
with codecs.open(os.path.join(ROOT_DIR, "_links.html"), 'r', 'utf-8') as linksFile:
	linksHtml = linksFile.read();


# Copy the contents of the curr html to it's deployed file but add in the
# links page
htmlFileContents = prog_add_links_to_page.sub(r'\1' + linksHtml, htmlFileContents)


# Insert a link to the CSS file. If we are in a subdir the link needs to
# adjusted to a relative path.
link_to_root = ""
htmlFileContents = 
	prog_css.sub(
		'<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" />'.format(
			link_to_root, "" if link_to_root == "" else '/'), 
		htmlFileContents)

newFileName = DST_FILE
targetDir = os.path.split(newFileName)[0]
if not os.path.isdir(targetDir):
	print("Creating {}".format(targetDir))
	os.makedirs(targetDir)

# Write out the new files
newFile = codecs.open(newFileName, 'w', 'utf-8')
newFile.write(htmlFileContents)
newFile.close()

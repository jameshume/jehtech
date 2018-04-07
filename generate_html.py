import sys
import os
import re
import subprocess
import codecs

SRC_FILE = sys.argv[1]
DST_FILE = sys.argv[2]

print("Generating {} from {}".format(DST_FILE, SRC_FILE))

def get_links_insert(currentDirName):
	return ""

def getMathjaxNodePageBinPath():
	cmd = "node -e \"console.log(require.resolve('mathjax-node-page'))\""
	result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	modpath = result.stdout.readlines()[0].strip().decode("utf-8") 
	basepath = os.path.split(os.path.split(modpath)[0])[0]
	exepath = os.path.join(basepath, 'bin', 'mjpage')
	return exepath

# Regex to put in the links into all the HTML pages
prog     = re.compile('(<\s*div\s+id\s*=\s*"includedContent"\s*>)', re.IGNORECASE)
# Regexs to put in JS and CSS
prog_css = re.compile('(<!--\s*CSS_INSERT\s*-->)', re.IGNORECASE)
prog_js  = re.compile('(<!--\s*JAVASCRIPT_INSERT\s*-->)', re.IGNORECASE)
prog_img = re.compile('##IMG_DIR##')

# Open and read in the source file
htmlFile = codecs.open(SRC_FILE, 'r', 'utf-8')
htmlFileContents = htmlFile.read();
htmlFile.close()

# Copy the contents of the curr html to it's deployed file but add in the
# links page
#htmlFileContents = prog.sub(r'\1' + linksHtml, htmlFileContents)
#htmlFileContents = prog_css.sub('<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" />'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
#htmlFileContents = prog_js.sub('<script src="{}{}jeh-monolith.js"></script>'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
#htmlFileContents = prog_img.sub('{}{}images/jeh-tech'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
newFileName = DST_FILE
targetDir = os.path.split(newFileName)[0]
if os.path.isdir(targetDir):
	print("Creating {}".format(targetDir))
	os.makedirs(targetDir)

# Write out the new files
newFile = codecs.open(newFileName, 'w', 'utf-8')
newFile.write(htmlFileContents)
newFile.close()

# Post process the HTML file to pre-render any MathJax
if platform.system() == 'Windows':
	mathjaxPageExe = getMathjaxNodePageBinPath()
	shutil.copyfile(newFileName, newFileName + ".TMP")
	cmd = 'node {} --dollars true < "{}" > {}'.format(mathjaxPageExe, newFileName + ".TMP", newFileName)
	subprocess.call(cmd, shell=True)
	os.remove(newFileName + ".TMP")
else:
	print("### WARNING: Need to implement node-page call on linux")

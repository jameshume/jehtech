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
import watermark
import platform

DEPLOYED_DIR = '../__deployed'

def CopyImagesDir(srcDir, destDir):
    # Recurse through the image directory. Files in the first level do not get
    # watermarked, everything else, minus a few exceptions (the icons directory
    # and some specific files) will get watermarked as they're copied over -
    # original images not modified...

    if not os.path.exists(destDir):
        os.makedirs(destDir)

    first = True # Make destDir and copy over the first layer of files
    for root, dirs, files in os.walk(srcDir):
        commonLen = len(os.path.commonprefix([srcDir, root]))
        relativeRoot = root[commonLen:]
        if len(relativeRoot) and relativeRoot[0] in ["/", "\\"]:
            relativeRoot = relativeRoot[1:]

        no_watermark_filename = os.path.join(root, "no_watermark.txt")
        no_watermark_imgs = []
        if os.path.isfile(no_watermark_filename):
            with open(no_watermark_filename) as fh:
                no_watermark_imgs = [x.strip() for x in fh.readlines()]
                #print(no_watermark_imgs)

        for currdir in dirs:
            destD = os.path.join(destDir, relativeRoot, currdir)
            if not os.path.exists(destD):
                #print("CREATING", destD)
                os.makedirs(destD)

        for file in files:
            # copy and watermark
            file_extension = os.path.splitext(file)[1]
            if first or file_extension.lower() not in [".png", ".jpg"] or file in no_watermark_imgs:
                # just copy file
                #print("COPY" , os.path.join(root, file), "==>", os.path.join(destDir, relativeRoot, file))
                shutil.copy(os.path.join(root, file), os.path.join(destDir, relativeRoot, file))
            else:
                # create a watermarked copy
                #print("WATERMARK" , os.path.join(root, file), "==>", os.path.join(destDir, relativeRoot, file))
                watermark.WatermarkImage(os.path.join(root, file), os.path.join(destDir, relativeRoot, file))

        first = False

def GenerateRunningCheckSum(data, value):
    return zlib.adler32(data, value) & 0xffffffff

def combine_files(base_dir, dest_file, is_debug=False):
    #print("COMBINING", base_dir, dest_file)
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
        #print("Loading {}".format(indexInfoFilename))
        prevRunningCRC = pickle.load(open(indexInfoFilename, 'rb'))
        foundPrevRunningCRC = True

    # Only regenerate the unminimsed combination of all the JS files if need be
    regenerated = False
    if os.path.isfile(un_minimised_temp_aggregate_file) and foundPrevRunningCRC and (prevRunningCRC == runningCRC):
        #print('The contents of "{}" has not changed. Skipping regeneration step.'.format(base_dir))
        pass
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


def getMathjaxNodePageBinPath():
    cmd = "node -e \"console.log(require.resolve('mathjax-node-page'))\""
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    modpath = result.stdout.readlines()[0].strip().decode("utf-8") 
    basepath = os.path.split(os.path.split(modpath)[0])[0]
    exepath = os.path.join(basepath, 'bin', 'mjpage')
    return exepath


def deploy_site(specificFile, generateImages):
    # Delete any existing deployment and begin creating a new one...
    if specificFile is None:
        if os.path.isdir(DEPLOYED_DIR):
            shutil.rmtree(DEPLOYED_DIR)
        os.mkdir(DEPLOYED_DIR)

        # Combine javascript and CSS files into monoliths
        monoJsFilename  = os.path.join(DEPLOYED_DIR, 'jeh-monolith.js')
        combine_files("./javascript", monoJsFilename)

        monoCssFilename = os.path.join(DEPLOYED_DIR, 'jeh-monolith.css')
        combine_files("./css", monoCssFilename)

    # Regex to put in the links "page" into all the HTML pages
    prog = re.compile('(<\s*div\s+id\s*=\s*"includedContent"\s*>)', re.IGNORECASE)

    # Regexs to put in JS and CSS
    prog_css = re.compile('(<!--\s*CSS_INSERT\s*-->)', re.IGNORECASE)
    prog_js  = re.compile('(<!--\s*JAVASCRIPT_INSERT\s*-->)', re.IGNORECASE)
    prog_img = re.compile('##IMG_DIR##')
    prog_snippet = re.compile('##\s*INCLUDE\s*:\s*([\w.\\/]+)\s*##')

    last_dirname = None
    link_to_root = ""
    doc = None
    os.chdir('html')
    sitemap_list = []

    file_list = find_html_files('.') if specificFile is None else [os.path.split(specificFile)]
    for dirname, filename in file_list:
        print ("Processing {}".format(os.path.join(dirname, filename)))
        # If we have changed directory we must regenerate the links page so that the
        # links are relative to this new directory
        if dirname != last_dirname:
            link_to_root = get_relative_to_root(dirname)
            linksHtml = get_links_insert(dirname)
            last_dirname = dirname

        # Read in the current HTML files contents
        htmlFileName = os.path.join(dirname, filename)
        #print("Deploying", dirname, filename, htmlFileName)


        if fnmatch.fnmatch(filename, '*.html'):
            ## dirty hackery
            dirs = list(os.path.split(dirname))
            if len(dirs) > 1:
                if dirs[0] == ".":
                    dirs = dirs[1:]

            dirs.append(filename)
            google_sitemap_ref = "http://www.jeh-tech.com/{}".format(pathlib.PurePosixPath(*dirs))
            sitemap_list.append(google_sitemap_ref)


        # Do we need toass the file through M4?
        req_m4 = False
        if fnmatch.fnmatch(filename, '*.html') and filename != "m4.html":
            with codecs.open(htmlFileName, 'r', 'utf-8') as htmlFile:
                firstline = htmlFile.readline().strip();
                req_m4 = firstline == 'dnl USEM4'

        if req_m4:
            result = subprocess.run(
                ['m4', htmlFileName], stdout=subprocess.PIPE, universal_newlines=True)
            htmlFileContents = result.stdout.strip()
        else:
            #htmlFile = codecs.open(htmlFileName, 'r', 'utf-8')
            with codecs.open(htmlFileName, 'r', 'utf-8') as htmlFile:
                htmlFileContents = htmlFile.read();
            #htmlFile.close()

        # Create and open the file in the deployed folder.
        deployed_dir = os.path.join('..', DEPLOYED_DIR, dirname)
        if (dirname != '.'):
            if not os.path.exists(deployed_dir):
                if specificFile is None:
                    mkdir_p(deployed_dir)
            newFileName = os.path.join('..', DEPLOYED_DIR, dirname, filename)
        else:
            newFileName = os.path.join('..', DEPLOYED_DIR, filename)

        # Copy the contents of the curr html to it's deployed file but add in the
        # links page
        htmlFileContents = prog.sub(r'\1' + linksHtml, htmlFileContents)
        htmlFileContents = prog_css.sub('<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" />'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
        htmlFileContents = prog_js.sub('<script src="{}{}jeh-monolith.js"></script>'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)
        htmlFileContents = prog_img.sub('{}{}images/jeh-tech'.format(link_to_root, "" if link_to_root == "" else '/'), htmlFileContents)

        # Lazy shitty coding
        def snippet_replace(matchobj):
            xhtmlFileName = os.path.join(dirname, matchobj.group(1))
            xhtmlFile = codecs.open(xhtmlFileName, 'r', 'utf-8')
            xhtmlFileContents = xhtmlFile.read();
            xhtmlFile.close()
            return xhtmlFileContents;
        htmlFileContents = prog_snippet.sub(snippet_replace, htmlFileContents)

        #print("Opening {} from {}".format(newFileName, os.getcwd()))
        newFile = codecs.open(newFileName, 'w', 'utf-8')
        newFile.write(htmlFileContents)
        newFile.close()

        if filename in ['math_revision.html', 'linear_alg.html', 'gaussians.html', 'stats.html', 'notes.html', 'gas-networks.html', 'spin.html']:
            mathjaxPageExe = getMathjaxNodePageBinPath()
            shutil.copyfile(newFileName, newFileName + ".TMP")
            print("   Parsing mathjax...")
            cmd = 'node {} --dollars true < "{}" > {}'.format(mathjaxPageExe, newFileName + ".TMP", newFileName)
            subprocess.call(cmd, shell=True)
            os.remove(newFileName + ".TMP")
    os.chdir('..')

    if specificFile is None:
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
                if filename == 'images' and generateImages:
                    target = os.path.join(DEPLOYED_DIR, filename)
                    CopyImagesDir(filename, target)
                else:
                    target = os.path.join(DEPLOYED_DIR, filename)
                    if os.path.isdir(filename):
                        #print("Copying directory", filename, "to", target)
                        shutil.copytree(filename, target)
                    elif os.path.isfile(filename):
                        #print("Copying file", filename, "to", target)
                        shutil.copy(filename, target)
                    else:
                        raise Exception('### WARNING: {} not copied!'.format(filename))
            else:
                raise Exception('### WARNING: {} does not exist!'.format(filename))


if __name__ == "__main__":
    import argparse
    try:

        parser = argparse.ArgumentParser(description="Generate JEH-Tech Website")
        parser.add_argument("-n", "--no_images", action="store_const", const=True)
        parser.add_argument("-f", "--file", action = "store")
        args = parser.parse_args()
        deploy_site(args.file, not args.no_images)
    except:
        #if os.path.isdir(DEPLOYED_DIR):
        #   shutil.rmtree(DEPLOYED_DIR)
        raise
        pass

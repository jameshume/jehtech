""" Some of the JEHTech pages have a (terrible!) way of inserting raw text files into the HTML
page inside <pre> tags. These HTML pages DEPEND on the text files, so if the text file changes
the HTML should be regenerated. Script outputs to a dependency file.
"""
import codecs
import re
import sys
from pathlib import Path

from snippet_regular_expressions import (RAW_FILE_INSERT_REGEX, ESCAPED_FILE_INSERT_REGEX)

SRC_ROOT = Path(sys.argv[1])
DST_ROOT = Path(sys.argv[2])
SRC_FILENAME = Path(sys.argv[3])
DEP_FILENAME = Path(sys.argv[4])
SRC_DIRNAME = SRC_FILENAME.parent


if __name__ == '__main__':
    dependee_filenames = []
    prog_snippet = re.compile(RAW_FILE_INSERT_REGEX)
    prog_escaped_snippet = re.compile(ESCAPED_FILE_INSERT_REGEX)

    with codecs.open(SRC_FILENAME, 'r', 'utf-8') as htmlFile:
        htmlFileContents = htmlFile.read()
        
        matches = prog_snippet.search(htmlFileContents)
        if matches is not None:
            dependee_filenames.append(str(SRC_DIRNAME / matches.group(1)))
        
        matches = prog_escaped_snippet.search(htmlFileContents)
        if matches is not None:
            dependee_filenames.append(str(SRC_DIRNAME / matches.group(1)))

    DEP_FILENAME.parent.mkdir(parents=True, exist_ok=True)
    with open(DEP_FILENAME, 'w', encoding='ascii') as dependencyFile:
        target = DST_ROOT / SRC_FILENAME.relative_to(SRC_ROOT)
        if len(dependee_filenames) > 0:
            dependencyFile.write(f"{target}: {' '.join(dependee_filenames)}\n")
        else:
            dependencyFile.write(f"{target}:\n")

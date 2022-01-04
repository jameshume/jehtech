""" Some of the JEHTech pages have a (terrible!) way of inserting raw text files into the HTML
page inside <pre> tags, so that notes are easily imported into a page that contains the site's
page HTML structure. There are different types of imports. The first is a raw import where the
referenced file's contents is dumped, without any processing, into a <pre></pre> block. The
second is when the file's contents are escaped so that HTML special characters are escaped.
Both formats can include images using the string "##IMG:...##", which will end the <pre> block
before the image, insert the image and then re-open the <pre> block for more text.

Eventually would like to move everything to a markdown format rather than this adhoc notes
structure.
"""
import codecs
import re
import sys
from pathlib import Path
import markdown

from snippet_regular_expressions import (
    PRE_TAG_IMG_SPLIT_REGEX, RAW_FILE_INSERT_REGEX, ESCAPED_FILE_INSERT_REGEX, MARKDOWN_FILE_REGEX
)


FILENAME = Path(sys.argv[1])
SNIPPET_DIRNAME = Path(sys.argv[2])
BASE_IMG_DIR = Path(sys.argv[3])


def split_pre_tags_for_images(xhtmlFileContents):
    """ In snippet contents, replace ##IMG:...## with </pre><img src="..."/><pre> """
    prog_img_in_escaped_snip = re.compile(PRE_TAG_IMG_SPLIT_REGEX)
    return prog_img_in_escaped_snip.sub(
        lambda mobj: f'</pre><img src="{BASE_IMG_DIR}/{mobj.group(1)}"/><pre>',
        xhtmlFileContents
    )


def inject_raw_snippet(match_object_for_snippet_placeholder):
    """ Include snippets - these are files who's contents are just dumped, raw, into a <pre>
    tag.
    """
    raw_snippet_filename =  SNIPPET_DIRNAME / match_object_for_snippet_placeholder.group(1)
    with codecs.open(raw_snippet_filename, 'r', 'utf-8') as raw_snippet_file:
        return raw_snippet_file.read()


def inject_markdown_snippet(match_object_for_snippet_placeholder):
    """ Include a markdown file, converted to HTML, as a snippet """
    md_filname = SNIPPET_DIRNAME / match_object_for_snippet_placeholder.group(1)
    with codecs.open(md_filname, 'r', 'utf-8') as md_file:
        return markdown.markdown(md_file.read())


def inject_processed_snippet(match_object_for_snippet_placeholder):
    """ Include escaped snippets - these are files who's contents are parsed to escape HTML
    characters, the result being dumped into a <pre> tag and replace and replace
    ##IMG:...## with </pre><img src="..."/><pre> so that <ore> tags can be split to
    accomodate images.
    """
    xhtmlFileName = SNIPPET_DIRNAME / match_object_for_snippet_placeholder.group(1)
    xhtmlFileContents = ""
    html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;"}

    with codecs.open(xhtmlFileName, 'r', 'utf-8') as xhtmlFile:
        xhtmlFileContents = xhtmlFile.readlines()
        ## Replace all ========== titles with <h1> tags
        ## Replace all HTML special characters with their escaped versions
        ## https://wiki.python.org/moin/EscapingHtml
        foundTitle = 0
        lookingForFinisher = False
        seenFirstHeading = False
        firstHeadingLine = -1
        for idx, line in enumerate(xhtmlFileContents):
            if line.strip()[:40] == ("=" * 40):
                if lookingForFinisher:
                    lookingForFinisher = False
                    foundTitle = 0
                    xhtmlFileContents[idx-1] = xhtmlFileContents[idx-1] + "</h2>"
                    xhtmlFileContents[idx] = "<pre>"
                else:
                    foundTitle += 1
            else:
                if foundTitle == 2:
                    xhtmlFileContents[idx] = xhtmlFileContents[idx].title()
                foundTitle = 0
                xhtmlFileContents[idx] = "".join(
                    html_escape_table.get(c, c) for c in xhtmlFileContents[idx])
            if foundTitle == 2:
                if firstHeadingLine == -1:
                    firstHeadingLine = idx - 1
                xhtmlFileContents[idx - 1] = ""
                if seenFirstHeading:
                    xhtmlFileContents[idx] = "</pre><h2>"
                else:
                    xhtmlFileContents[idx] = "<h2>"
                    seenFirstHeading = True
                lookingForFinisher = True
        if firstHeadingLine == -1 or firstHeadingLine > 0:
            xhtmlFileContents = "<pre>" + "".join(xhtmlFileContents) + "</pre>"
        else:
            xhtmlFileContents = "".join(xhtmlFileContents) + "</pre>"
    
    return xhtmlFileContents


if __name__ == '__main__':
        prog_snippet = re.compile(RAW_FILE_INSERT_REGEX)
        prog_escaped_snippet = re.compile(ESCAPED_FILE_INSERT_REGEX)
        prog_markdown_snippet = re.compile(MARKDOWN_FILE_REGEX)

        htmlFileContents = ""
        with codecs.open(FILENAME, 'r', 'utf-8') as htmlFile:
            htmlFileContents = prog_snippet.sub(inject_raw_snippet, htmlFile.read())
            htmlFileContents = prog_escaped_snippet.sub(inject_processed_snippet, htmlFileContents)
            htmlFileContents = prog_markdown_snippet.sub(inject_markdown_snippet, htmlFileContents)
            htmlFileContents = split_pre_tags_for_images(htmlFileContents)

        with codecs.open(FILENAME, 'w', 'utf-8') as htmlFile:
            htmlFile.write(htmlFileContents)
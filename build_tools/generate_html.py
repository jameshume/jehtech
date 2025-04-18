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

print("generate_html.py: Generating {} from {}".format(DST_FILE, SRC_FILE))

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
hack_css = """pre { line-height: 105%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
pre code .hll { background-color: #ffffcc }
pre code { background: #f8f8f8; }
pre code .c { color: #3D7B7B; font-style: italic } /* Comment */
pre code .err { border: 1px solid #FF0000 } /* Error */
pre code .k { color: #008000; font-weight: bold } /* Keyword */
pre code .o { color: #666666 } /* Operator */
pre code .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
pre code .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
pre code .cp { color: #9C6500 } /* Comment.Preproc */
pre code .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
pre code .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
pre code .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
pre code .gd { color: #A00000 } /* Generic.Deleted */
pre code .ge { font-style: italic } /* Generic.Emph */
pre code .ges { font-weight: bold; font-style: italic } /* Generic.EmphStrong */
pre code .gr { color: #E40000 } /* Generic.Error */
pre code .gh { color: #000080; font-weight: bold } /* Generic.Heading */
pre code .gi { color: #008400 } /* Generic.Inserted */
pre code .go { color: #717171 } /* Generic.Output */
pre code .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
pre code .gs { font-weight: bold } /* Generic.Strong */
pre code .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
pre code .gt { color: #0044DD } /* Generic.Traceback */
pre code .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
pre code .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
pre code .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
pre code .kp { color: #008000 } /* Keyword.Pseudo */
pre code .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
pre code .kt { color: #B00040 } /* Keyword.Type */
pre code .m { color: #666666 } /* Literal.Number */
pre code .s { color: #BA2121 } /* Literal.String */
pre code .na { color: #687822 } /* Name.Attribute */
pre code .nb { color: #008000 } /* Name.Builtin */
pre code .nc { color: #0000FF; font-weight: bold } /* Name.Class */
pre code .no { color: #880000 } /* Name.Constant */
pre code .nd { color: #AA22FF } /* Name.Decorator */
pre code .ni { color: #717171; font-weight: bold } /* Name.Entity */
pre code .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
pre code .nf { color: #0000FF } /* Name.Function */
pre code .nl { color: #767600 } /* Name.Label */
pre code .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
pre code .nt { color: #008000; font-weight: bold } /* Name.Tag */
pre code .nv { color: #19177C } /* Name.Variable */
pre code .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
pre code .w { color: #bbbbbb } /* Text.Whitespace */
pre code .mb { color: #666666 } /* Literal.Number.Bin */
pre code .mf { color: #666666 } /* Literal.Number.Float */
pre code .mh { color: #666666 } /* Literal.Number.Hex */
pre code .mi { color: #666666 } /* Literal.Number.Integer */
pre code .mo { color: #666666 } /* Literal.Number.Oct */
pre code .sa { color: #BA2121 } /* Literal.String.Affix */
pre code .sb { color: #BA2121 } /* Literal.String.Backtick */
pre code .sc { color: #BA2121 } /* Literal.String.Char */
pre code .dl { color: #BA2121 } /* Literal.String.Delimiter */
pre code .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
pre code .s2 { color: #BA2121 } /* Literal.String.Double */
pre code .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
pre code .sh { color: #BA2121 } /* Literal.String.Heredoc */
pre code .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
pre code .sx { color: #008000 } /* Literal.String.Other */
pre code .sr { color: #A45A77 } /* Literal.String.Regex */
pre code .s1 { color: #BA2121 } /* Literal.String.Single */
pre code .ss { color: #19177C } /* Literal.String.Symbol */
pre code .bp { color: #008000 } /* Name.Builtin.Pseudo */
pre code .fm { color: #0000FF } /* Name.Function.Magic */
pre code .vc { color: #19177C } /* Name.Variable.Class */
pre code .vg { color: #19177C } /* Name.Variable.Global */
pre code .vi { color: #19177C } /* Name.Variable.Instance */
pre code .vm { color: #19177C } /* Name.Variable.Magic */
pre code .il { color: #666666 } /* Literal.Number.Integer.Long */
"""
print(f"Hack CSS is '{hack_css}'")
print('<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" /><style>{}</style>'.format(
		link_to_root, 
		"" if link_to_root == "" else '/', 
		hack_css
	))
htmlFileContents = prog_css.sub(
	'<link rel="stylesheet" href="{}{}jeh-monolith.css" type="text/css" /><style>{}</style>'.format(
		link_to_root, 
		"" if link_to_root == "" else '/', 
		hack_css
	),
	htmlFileContents
)

newFileName = DST_FILE
targetDir = os.path.split(newFileName)[0]
if not os.path.isdir(targetDir):
	print("Creating {}".format(targetDir))
	os.makedirs(targetDir)

# Write out the new files
newFile = codecs.open(newFileName, 'w', 'utf-8')
newFile.write(htmlFileContents)
newFile.close()

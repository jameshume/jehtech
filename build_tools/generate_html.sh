#!/bin/bash

function get_relative_dir_path_prefix() {
    # Function assumes that the image directory is an immediate subdirectory
    # of the root HTML directory.
    local html_file_path     # This should include the html file
    local html_root_dir_path # This is a path to the root HTML directory
    html_file_path="$1"
    html_root_dir_path="$2"

    mapfile -d "/"  file_ary <<< "${html_file_path}"
    mapfile -d "/"  root_ary <<< "${html_root_dir_path}"

    file_ary_len=${#file_ary[@]}
    root_ary_len=${#root_ary[@]}
    distance="$((file_ary_len - root_ary_len - 1))"
    if [ "${distance}" == "0" ]; then
        printf ''
    else
        printf '../%.0s' $(seq  1 ${distance})
    fi
}

DEBUG_TMP=$(mktemp)

SRC=$1
DST=$2
DEBUG_OUT_FILE="${DST}.debug.txt"

function err_handler() {
    echo -e "\\n-----------------------------------------"
    echo "An error occurred with status $1" >> "${DEBUG_OUT_FILE}"
    echo "Stack trace is:" >> "${DEBUG_OUT_FILE}"
    i=0; while caller $i >> "${DEBUG_OUT_FILE}"; do (( i=i+1 )); done
}
trap "err_handler $?" ERR
set -o pipefail
set -o errtrace

ROOT_IMAGES_RELATIVE_TO=$3
RELATIVE_PREFIX="$(get_relative_dir_path_prefix "${DST}" "${ROOT_IMAGES_RELATIVE_TO}")"
IMG_DIR="${RELATIVE_PREFIX}images/jeh-tech"
echo "Generating $(realpath ${DST}) from $(realpath ${SRC})"

echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "SRC >>>>>>>>" >> "${DEBUG_OUT_FILE}"
cat "${SRC}" >> "${DEBUG_OUT_FILE}"
echo "<<<<<<<< SRC" >> "${DEBUG_OUT_FILE}"

# All files that use M4 preprocessor must include the line "dnl USEM4".
if grep --ignore-case "dnl USEM4" "${SRC}" > /dev/null
then
    echo "   Running M4 macro expansion for ${SRC}"
    m4 "${SRC}" > "${DST}"
    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "POST M4 EXPANSION:" >> "${DEBUG_OUT_FILE}"
else
    cp "${SRC}" "${DST}"
    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "POST NO M4 EXPANSION JUST COPY:" >> "${DEBUG_OUT_FILE}"
fi
cat "${DST}" >> "${DEBUG_OUT_FILE}"

# All files that contain MathJax to be be pre-processed should have the string "<!-- MATHJAX -->"
# somewhere in the file. Its easier doing this than it is to "guess" as to whether the HTML
# contains MathJax by trying to, for example, parse the HTML to see if there is MathJax content.
# Want to avoid trying to render pages with no MathJax as it increases build time noticably.
if grep --ignore-case "<!--\s*MATHJAX\s*-->" "${DST}" > /dev/null
then
    echo "   Pre-rendering MathJax for ${DST}"
    TMP=$(mktemp)
    node -r esm tex2html-cpage.js "${DST}" > "${TMP}"
    mv "${TMP}" "${DST}"

    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
    echo "POST MATHJAX:" >> "${DEBUG_OUT_FILE}"
    cat "${DST}" >> "${DEBUG_OUT_FILE}"
fi

# Process snippet inserts - must be done before all other in-place sed'ing
# Process the destination file but give the dirname of the source file so that
# the snippet can be found.
python3 process_snippets.py "${DST}" "$(dirname "${SRC}")" "${IMG_DIR}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "POST SNIPPETS:" >> "${DEBUG_OUT_FILE}"
cat "${DST}" >> "${DEBUG_OUT_FILE}"

# Each file contains a marker that must be replaced with the contents of the _link.html page
# NOTE: <div id="includedContent"> must have the closing tag on the SAME LINE and be one a
#       line OF ITS OWN! The links must also be modified for files in subdirectories so that
#       the link gives the correct relative path to the target.
links_tmp_file="$(mktemp)"
cp "../src/html/_links.html" "${links_tmp_file}"
sed --in-place -e  "s#href=\"\([^\"]*\)\"#href=\"${RELATIVE_PREFIX}\1\"#g" "${links_tmp_file}"
sed --in-place -e "/\(<\s*div\s\s*id\s*=\s*\"includedContent\"\s*>\)/{r ${links_tmp_file}
d}" "${DST}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "POST LINKS:" >> "${DEBUG_OUT_FILE}"
cat "${DST}" >> "${DEBUG_OUT_FILE}"

# Each file contains a marker for the CSS import that must use a *relative* import directory
# from this page to the CSS file. 
hack_css="pre { line-height: 105%; }
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
"
sed --in-place  -e \
    "s#<!--\s*CSS_INSERT\s*-->#<link rel=\"stylesheet\" href=\"${RELATIVE_PREFIX}jeh-monolith.css\" type=\"text/css\" /><style>${hackcss//$'\n'/\\n}</style>#" \
    "${DST}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
cat "${DST}" >> "${DEBUG_OUT_FILE}"
echo "POST CSS:" >> "${DEBUG_OUT_FILE}"

# Each file contains a marker for the JavaScript import that must use a *relative* import
# directory from this page to the JavaScript file. 
sed --in-place  -e \
    "s#<!--\s*JAVASCRIPT_INSERT\s*-->#<script src=\"${RELATIVE_PREFIX}jeh-monolith.js\"></script>#" \
    "${DST}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
cat "${DST}" >> "${DEBUG_OUT_FILE}"
echo "POST JAVASCRIPT:" >> "${DEBUG_OUT_FILE}"

# The ##IMG_DIR## marker must be replaced with the path to the image directory on the server
sed --in-place  -e "s|##IMG_DIR##|${IMG_DIR}|" "${DST}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
echo "=============================================================================================" >> "${DEBUG_OUT_FILE}"
cat "${DST}" >> "${DEBUG_OUT_FILE}"
echo "POST IMG_DIR:" >> "${DEBUG_OUT_FILE}"

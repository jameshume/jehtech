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

SRC=$1
DST=$2
ROOT_IMAGES_RELATIVE_TO=$3
RELATIVE_PREFIX="$(get_relative_dir_path_prefix "${DST}" "${ROOT_IMAGES_RELATIVE_TO}")"
IMG_DIR="${RELATIVE_PREFIX}images/jeh-tech"
echo "Generating ${DST} from ${SRC}"

# All files that use M4 preprocessor must include the line "dnl USEM4".
if grep --ignore-case "dnl USEM4" "${DST}" > /dev/null
then
    echo "   Running M4 macro expansion for ${DST}"
    TMP=$(mktemp)
    m4 "${DST}" > "${TMP}"
    mv "${TMP}" "${DST}"
fi

# All files that contain MathJax to be be pre-processed should have the string "<!-- MATHJAX -->"
# somewhere in the file. Its easier doing this than it is to "guess" as to whether the HTML
# contains MathJax by trying to, for example, parse the HTML to see if there is MathJax content.
# Want to avoid trying to render pages with no MathJax as it increases build time noticably.
if grep --ignore-case "<!--\s*MATHJAX\s*-->" "${SRC}" > /dev/null
then
    echo "   Pre-rendering MathJax for ${SRC}"
    node -r esm tex2html-cpage.js "${SRC}" > "${DST}"
else
    cp "${SRC}" "${DST}"
fi

# Process snippet inserts - must be done before all other in-place sed'ing
# Process the destination file but give the dirname of the source file so that
# the snippet can be found.
python3 process_snippets.py "${DST}" "$(dirname "${SRC}")" "${IMG_DIR}"

# Each file contains a marker that must be replaced with the contents of the _link.html page
# NOTE: <div id="includedContent"> must have the closing tag on the SAME LINE and be one a
#       line OF ITS OWN! The links must also be modified for files in subdirectories so that
#       the link gives the correct relative path to the target.
links_tmp_file="$(mktemp)"
cp "../src/html/_links.html" "${links_tmp_file}"
sed --in-place -e  "s#href=\"\([^\"]*\)\"#href=\"${RELATIVE_PREFIX}\1\"#g" "${links_tmp_file}"
sed --in-place -e "/\(<\s*div\s\s*id\s*=\s*\"includedContent\"\s*>\)/{r ${links_tmp_file}
d}" "${DST}"

# Each file contains a marker for the CSS import that must use a *relative* import directory
# from this page to the CSS file. 
sed --in-place  -e \
    "s#<!--\s*CSS_INSERT\s*-->#<link rel=\"stylesheet\" href=\"${RELATIVE_PREFIX}jeh-monolith.css\" type=\"text/css\" />#" \
    "${DST}"

# Each file contains a marker for the JavaScript import that must use a *relative* import
# directory from this page to the JavaScript file. 
sed --in-place  -e \
    "s#<!--\s*JAVASCRIPT_INSERT\s*-->#<script src=\"${RELATIVE_PREFIX}jeh-monolith.js\"></script>#" \
    "${DST}"

# The ##IMG_DIR## marker must be replaced with the path to the image directory on the server
sed --in-place  -e "s|##IMG_DIR##|${IMG_DIR}|" "${DST}"

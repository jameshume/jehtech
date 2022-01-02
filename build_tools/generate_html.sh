SRC=$1
DST=$2

echo "Generating ${DST} from ${SRC}"

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


# All files that use M4 preprocessor must include the line "dnl USEM4".
if grep --ignore-case "dnl USEM4" "${DST}" > /dev/null
then
    echo "   Running M4 macro expansion for ${SRC}"
    TMP=$(mktemp)
    m4 "${DST}" > "${TMP}"
    cp "${TMP}" "${DST}"
fi

# Process snippet inserts - must be done before all other in-place sed'ing
python3 process_snippets.py "${SRC}" "${DST}" "images/jeh-tech"

# Each file contains a marker that must be replaced with the contents of the _link.html page
# NOTE: <div id="includedContent"> must have the closing tag on the SAME LINE and be one a
#       line OF ITS OWN!
sed --in-place  -e '/\(<\s*div\s\s*id\s*=\s*"includedContent"\s*>\)/{r ../src/html/_links.html
d}' "${DST}"

# Each file contains a marker for the CSS import that must use a *relative* import directory
# from this page to the CSS file. 
sed --in-place  -e 's#<!--\s*CSS_INSERT\s*-->#<link rel="stylesheet" href="jeh-monolith.css" type="text/css" />#' "${DST}"

# Each file contains a marker for the JavaScript import that must use a *relative* import
# directory from this page to the JavaScript file. 
sed --in-place  -e 's#<!--\s*JAVASCRIPT_INSERT\s*-->#<script src="jeh-monolith.js"></script>#' "${DST}"

# The ##IMG_DIR## marker must be replaced with the path to the image directory on the server
sed --in-place  -e 's$##IMG_DIR##$images/jeh-tech$' "${DST}"

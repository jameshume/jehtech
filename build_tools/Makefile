SRC_DIR:=../src
SRC_HTML_ROOT_DIR:=$(SRC_DIR)/html
SRC_HTML_DIRS:=$(shell find "$(SRC_HTML_ROOT_DIR)" -type d)
SRC_HTML_FILES:=$(shell find "$(SRC_HTML_ROOT_DIR)" -type f -name "*.html")

SRC_IMAGE_DIR:=$(SRC_DIR)/images
SRC_IMAGE_FILES:=$(shell find "$(SRC_IMAGE_DIR)" -type f)
SRC_IMAGE_FILES:=$(filter %.png %.gif %.mp4 %.svg %.jpg %.jpeg %.tif,$(SRC_IMAGE_FILES))

SRC_JAVASCRIPT_DIR:=$(SRC_DIR)/javascript
SRC_JAVASCRIPT_FILES := $(shell find "$(SRC_JAVASCRIPT_DIR)" -type f -name "*.js")

SRC_CSS_DIR:=$(SRC_DIR)/css
SRC_CSS_FILES := $(shell find "$(SRC_CSS_DIR)" -type f -name "*.css")

OUTPUT_DIR=../output

DST_HTML_ROOT_DIR:=$(OUTPUT_DIR)/site
DST_HTML_DIRS:=$(patsubst $(SRC_HTML_ROOT_DIR)%,$(DST_HTML_ROOT_DIR)%,$(SRC_HTML_DIRS))
DST_HTML_FILES:=$(patsubst $(SRC_HTML_ROOT_DIR)%,$(DST_HTML_ROOT_DIR)%,$(SRC_HTML_FILES))
DST_IMAGE_DIR:=$(DST_HTML_ROOT_DIR)/images
DST_IMAGE_FILES:=$(patsubst $(SRC_IMAGE_DIR)%,$(DST_IMAGE_DIR)%,$(SRC_IMAGE_FILES))

DEP_DIR:=$(OUTPUT_DIR)/deps
DEP_FILES:=$(patsubst %.html,%.d,$(patsubst $(DST_HTML_ROOT_DIR)%,$(DEP_DIR)%,$(DST_HTML_FILES)))

#
# MACRO generates the HTML rules that take HTML files from the source directory into the built
# directory.
#
# The dependencies are a little note worthy: the output-html file is dependent on snippets in
# the source directory - the src-html file is *not* dependent on the snippet as this doesn't
# get generated!
#
# Args:
#    $1 - The root *source* HTML directory
#    $2 - The *source* HTML directory under and including $1 that will be mirrored in the built
#         directory.
#    $3 - The root *destination* HTML directory
define generate_html_rules
$(patsubst $(1)%,$(DEP_DIR)%,$(2))/%.d:
	@python3 generate_snippet_dependencies.py \
        "$(1)" \
        "$(3)" \
        "$$(patsubst %.d,%.html,$$(patsubst $(DEP_DIR)%,$(1)%,$$@))" \
        "$$@"

$(patsubst $(1)%,$(3)%,$(2))/%.html: $(2)/%.html $(1)/_links.html $(patsubst $(1)%,$(DEP_DIR)%,$(2))/%.d | $(patsubst $(1)%,$(3)%,$(2)) $(patsubst $(1)%,$(DEP_DIR)%,$(2))
	@./generate_html.sh "$$<" "$$@"

$(patsubst $(1)%,$(3)%,$(2)):
	@mkdir --parents "$$@"

$(patsubst $(1)%,$(DEP_DIR)%,$(2)):
	@mkdir --parents "$$@"
endef


#
# MACRO generates the site images, most of which are watermarked versions of the source images.
#
# Args:
#    $1 - The source image file
define generate_images_rules
$(patsubst $(SRC_IMAGE_DIR)%,$(DST_IMAGE_DIR)%,$(1)): $(1)
	@echo "Generating $$@"
	@mkdir --parents "$$$$(dirname "$$@")" 1>/dev/null 2>&1 || true
	@cp "$$<" "$$@"
endef


.PHONY: all
all: images html javascript css | $(OUTPUT_DIR)
	@echo DONE


.PHONY: images
images: $(DST_IMAGE_FILES)


.PHONY: html
html: $(DST_HTML_FILES)


.PHONY: javascript
javascript: $(DST_HTML_ROOT_DIR)/jeh-monolith.js


.PHONY: css
css: $(DST_HTML_ROOT_DIR)/jeh-monolith.css


.PHONY: clean_html
clean_html:
	@rm -fr $(DST_HTML_FILES) $(DEP_DIR)


.PHONY: clean_javascript
clean_javascript:
	@rm -fr $(DST_HTML_ROOT_DIR)/jeh-monolith.js


.PHONY: clean_css
clean_css:
	@rm -fr $(DST_HTML_ROOT_DIR)/jeh-monolith.css


.PHONY: clean
clean:
	@rm -fr $(OUTPUT_DIR)


# The JavaScript monolith is supposed to reduce the number of seperate requrest that the browser
# has to make to get all the different JavaScript components required by the pages. It
# consists of a loads of JS files concatenated together and then minified.
#
# Note: jeh-*.js files depend on JQuery so these are appended to the monolith last.
$(DST_HTML_ROOT_DIR)/jeh-monolith.js: $(SRC_JAVASCRIPT_FILES)
	@echo "Generating $@"
	@rm -f "$@"
	@for file in $(filter-out %jeh-tech.js %jeh-tech-canvas.js,$(SRC_JAVASCRIPT_FILES)); \
     do \
        echo "   Packing $${file}"; \
        cat "$${file}" >> "$@"; \
     done
	@for file in $(filter %jeh-tech.js %jeh-tech-canvas.js,$(SRC_JAVASCRIPT_FILES)); \
     do \
        echo "   Packing $${file}"; \
        cat "$${file}" >> "$@"; \
     done
	@echo "   Minifying..."
	@node-minify --compressor uglify-es --input "$@" --output "$@" --silence


# The CSS monolith is supposed to reduce the number of seperate requrest that the browser
# has to make to get all the different CSS components required by the pages. It
# consists of a loads of CSS files concatenated together and then minified.
$(DST_HTML_ROOT_DIR)/jeh-monolith.css: $(SRC_CSS_FILES)
	@echo "Generating $@"
	@rm -f "$@"
	@for file in $(SRC_CSS_FILES); do cat "$${file}" >> "$@"; done
	@node-minify --compressor cssnano --input "$@" --output "$@" --silence


# The HTML file build rules. The macro is evaluated for each source HTML file so that a rule
# dest-html: src-html src-html-dep is created.
$(foreach image_file,$(SRC_IMAGE_FILES),$(eval $(call generate_images_rules,$(image_file))))


# The CSS file build rules. Macro evaluation similar to how HTML rule macro eval works.
$(foreach html_dir,$(SRC_HTML_DIRS),$(eval $(call generate_html_rules,$(SRC_HTML_ROOT_DIR),$(html_dir),$(DST_HTML_ROOT_DIR))))


# Make sure output dir exists
$(OUTPUT_DIR):
	mkdir --parents "$(OUTPUT_DIR)"

# Include the dependency files. These give a mapping from HTML files to any imported snippets
# If any of the include targets (i.e., the DEP_FILES) were updated by the rules the 
# makefile is reloaded with a cleared db.
#
# Note dependency files must be marked as SECONDARY so that make does not think they are
# normal intermediary files that should be clean up at the end of a build.
.SECONDARY: $(DEP_FILES)
include $(DEP_FILES)
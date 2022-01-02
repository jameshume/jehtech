DEPS_DIR:=deps

SRC_DIR:=../src
SRC_HTML_ROOT_DIR:=$(SRC_DIR)/html
SRC_HTML_DIRS:=$(shell find "$(SRC_HTML_ROOT_DIR)" -type d)
SRC_HTML_FILES:=$(shell find "$(SRC_HTML_ROOT_DIR)" -type f -name "*.html")

SRC_IMAGE_DIR:=$(SRC_DIR)/images
SRC_IMAGE_FILES:=$(shell find "$(SRC_IMAGE_DIR)" -type f)
SRC_IMAGE_FILES:=$(filter %.png %.gif %.mp4 %.svg %.jpg %.jpeg %.tif,$(SRC_IMAGE_FILES))

DST_DIR:=../output
DST_HTML_ROOT_DIR:=$(DST_DIR)/site
DST_HTML_DIRS:=$(patsubst $(SRC_HTML_ROOT_DIR)%,$(DST_HTML_ROOT_DIR)%,$(SRC_HTML_DIRS))
DST_HTML_FILES:=$(patsubst $(SRC_HTML_ROOT_DIR)%,$(DST_HTML_ROOT_DIR)%,$(SRC_HTML_FILES))

DST_IMAGE_DIR:=$(DST_HTML_ROOT_DIR)/images
DST_IMAGE_FILES:=$(patsubst $(SRC_IMAGE_DIR)%,$(DST_IMAGE_DIR)%,$(SRC_IMAGE_FILES))


#
# MACRO generates the HTML rules that take HTML files from the source directory into the built
# directory.
#
# For ease of reading, read "$(patsubst $(1)%,$(3)%,$(2))" as
# "source-html-dir transformed to dest-html-dir"
#
# Args:
#    $1 - The root *source* HTML directory
#    $2 - The *source* HTML directory under and including $1 that will be mirrored in the built
#         directory.
#    $3 - The root *destination* HTML directory
#
# Nice that this works but totally useless!
# python3 gen_image_dependencies.py "$$@" "$$(DST_DIR)" "$$(DEPS_DIR)" "$$(DST_IMAGE_DIR)"
define generate_html_rules
$(patsubst $(1)%,$(3)%,$(2))/%.html: $(2)/%.html $(1)/_links.html | $(patsubst $(1)%,$(3)%,$(2))
	@./generate_html.sh "$$<" "$$@"

$(patsubst $(1)%,$(3)%,$(2)):
	@mkdir --parents "$$@"
endef

$(foreach html_dir,$(SRC_HTML_DIRS),$(eval $(call generate_html_rules,$(SRC_HTML_ROOT_DIR),$(html_dir),$(DST_HTML_ROOT_DIR))))


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
$(foreach image_file,$(SRC_IMAGE_FILES),$(eval $(call generate_images_rules,$(image_file))))


.PHONY: all
all: images html | $(DST_DIR)
	@echo DONE


.PHONY: images
images: $(DST_IMAGE_FILES)


.PHONY: html
html: $(DST_HTML_FILES)


.PHONY: clean
clean:
	@rm -fr $(DST_DIR)
	@rm -fr $(DEPS_DIR)


$(DST_DIR):
	mkdir --parents "$(DST_DIR)"
	mkdir --parents "$(DST_HTML_ROOT_DIR)"
	mkdir --parents "$(DST_IMAGE_DIR)"
	mkdir --parents "$(DEPS_DIR)"



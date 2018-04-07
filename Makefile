ifeq ($(OS),Windows_NT)
define create_os_path
$(subst /,\\,$(1))
endef
else
define create_os_path
$(1)
endef
endif

DEPLOYMENT_DIR := __test
VPATH += src/html
BASE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
SRCS :=

include $(BASE_DIR)/src/html/module.mk

OBJS := $(patsubst $(BASE_DIR)/src/html/%,$(BASE_DIR)/__test/%,$(SRCS))

.PHONY: all
all: $(OBJS)

$(BASE_DIR)/__test/%.html: $(BASE_DIR)/src/html/%.html
	python $(BASE_DIR)/generate_html.py "$<" "$@"

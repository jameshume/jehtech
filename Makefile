ifeq ($(OS),Windows_NT)
   RMDIR := rmdir /S /Q
else
   RMDIR := rm -fr
endif

DEPLOYMENT_DIR := __test
VPATH += src/html
BASE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
SRCS :=

include $(BASE_DIR)/src/html/module.mk

OBJS := $(patsubst $(BASE_DIR)/src/html/%,$(BASE_DIR)/__test/%,$(SRCS))

.PHONY: all
all: $(OBJS)

.PHONY: clean
clean:
	$(RMDIR) $(DEPLOYMENT_DIR)

$(BASE_DIR)/__test/%.html: $(BASE_DIR)/src/html/%.html $(BASE_DIR)/src/html/_links.html
	python $(BASE_DIR)/generate_html.py "$<" "$@" "$(BASE_DIR)/src/html/_links.html"

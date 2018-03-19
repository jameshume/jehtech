BASE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
HTML_SOURCES :=

include src/html/module.mk

all:
	@echo "$(HTML_SOURCES)"
HTML_SOURCES += $(wildcard $(BASE_DIR)/src/html/*.html)

SUB_DIRS := $(sort $(dir $(wildcard $(BASE_DIR)/src/html/*/)))
include $(foreach dir,$(wordlist 2, $(words $(SUB_DIRS)), $(SUB_DIRS)),$(dir)module.mk)


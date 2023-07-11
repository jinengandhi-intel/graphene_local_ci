# Relative path to gramine root
THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
#GRAMINEDIR = ../..
GRAMINEDIR ?= $(THIS_DIR)../..
ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: bonnie++.manifest
ifeq ($(SGX),1)
all: bonnie++.manifest.sgx bonnie++.sig
endif

bonnie++.manifest: bonnie++.manifest.template
			gramine-manifest \
			-Dlog_level=$(GRAMINE_LOG_LEVEL) \
			-Darch_libdir=$(ARCH_LIBDIR) \
            $< > $@

bonnie++.manifest.sgx: bonnie++.manifest
			gramine-sgx-sign \
			--manifest $< --output $@

bonnie++.sig: bonnie++.manifest.sgx

.PHONY: clean
clean:
		$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader

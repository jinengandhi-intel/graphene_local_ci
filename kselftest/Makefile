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
all: kselftest.manifest
ifeq ($(SGX),1)
all: kselftest.manifest.sgx kselftest.sig
endif

kselftest.manifest: manifest.template
			gramine-manifest \
			-Dlog_level=$(GRAMINE_LOG_LEVEL) \
			-Darch_libdir=$(ARCH_LIBDIR) \
			-Dexecdir=$(shell dirname $(shell which bash)) \
            $< > $@

kselftest.manifest.sgx: kselftest.manifest
			gramine-sgx-sign \
			--manifest $< --output $@

kselftest.sig: kselftest.manifest.sgx

.PHONY: clean
clean:
		$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader

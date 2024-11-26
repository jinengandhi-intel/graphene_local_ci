ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
# Relative path to Graphene root
THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
#GRAPHENEDIR = ../..
GRAPHENEDIR ?= $(THIS_DIR)../..

TEST_LIST ?= sd_150_test_16gb.list

ifeq ($(DEBUG),1)
GRAPHENE_LOG_LEVEL = debug
else
GRAPHENE_LOG_LEVEL = error
endif

.PHONY: all
all: sd-test.manifest
ifeq ($(SGX),1)
all: sd-test.manifest.sgx sd-test.sig
endif

sd-test.manifest: sd-test.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAPHENE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		$< > $@

sd-test.manifest.sgx: sd-test.manifest
		gramine-sgx-sign \
		--manifest $< --output $@

sd-test.sig: sd-test.manifest.sgx


.PHONY: start-sd-test
start-sd-test: all
	gramine-sgx ./sd-test \
        	--on-crash=kill \
        	--no-memory-sampling \
        	--temperature-threshold=disable \
        	--test-delay=1000 \
        	-v \
        	-o stdout \
        	--disable mce_check \
		--test-list-file $(TEST_LIST)

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader


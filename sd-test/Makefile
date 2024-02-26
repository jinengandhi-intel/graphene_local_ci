ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
# Relative path to Graphene root
THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
#GRAPHENEDIR = ../..
GRAPHENEDIR ?= $(THIS_DIR)../..

ifeq ($(DEBUG),1)
GRAPHENE_LOG_LEVEL = debug
else
GRAPHENE_LOG_LEVEL = error
endif

.PHONY: all
all: sd-test.manifest
ifeq ($(SGX),1)
all: sd-test.manifest.sgx sd-test.sig sd-test.token
endif

sd-test.manifest: sd-test.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAPHENE_LOG_LEVEL) \
		-Darch_libdir=$(ARCH_LIBDIR) \
		$< > $@

sd-test.manifest.sgx: sd-test.manifest sd-test
		gramine-sgx-sign \
		--manifest $< --output $@

sd-test.sig: sd-test.manifest.sgx

sd-test.token: sd-test.sig
	gramine-sgx-get-token --output sd-test.token --sig sd-test.sig


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
		--test-list-file sd_150_test.list 


.PHONY: start-sd-test-16G
start-sd-test-16G: all
	gramine-sgx ./sd-test \
                --on-crash=kill \
                --no-memory-sampling \
                --temperature-threshold=disable \
                --test-delay=1000 \
                -v \
                -o stdout \
                --disable mce_check \
                --test-list-file sd_150_test_16GB.list


.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader


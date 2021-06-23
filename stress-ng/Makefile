# Relative path to Graphene root
THIS_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
#GRAPHENEDIR = ../..
GRAPHENEDIR ?= $(THIS_DIR)../..
SGX_SIGNER_KEY ?= $(GRAPHENEDIR)/Pal/src/host/Linux-SGX/signer/enclave-key.pem

ifeq ($(DEBUG),1)
GRAPHENE_LOG_LEVEL = debug
else
GRAPHENE_LOG_LEVEL = error
endif

.PHONY: all
all: stress-ng.manifest
ifeq ($(SGX),1)
all: stress-ng.manifest.sgx stress-ng.sig stress-ng.token
endif

include ../../Scripts/Makefile.configs

stress-ng.manifest: stress-ng.manifest.template
			graphene-manifest \
			-Dlog_level=$(GRAPHENE_LOG_LEVEL) \
			-Darch_libdir=$(ARCH_LIBDIR) \
            $< > $@

stress-ng.manifest.sgx: stress-ng.manifest
			graphene-sgx-sign \
			--key $(SGX_SIGNER_KEY) \
			--manifest $< --output $@

stress-ng.sig: stress-ng.manifest.sgx

stress-ng.token: stress-ng.sig
		graphene-sgx-get-token --output stress-ng.token --sig stress-ng.sig

.PHONY: clean
clean:
		$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader

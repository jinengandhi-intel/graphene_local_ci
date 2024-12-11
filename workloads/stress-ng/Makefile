# Relative path to gramine root
ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: stress-ng.manifest
ifeq ($(SGX),1)
all: stress-ng.manifest.sgx stress-ng.sig
endif

stress-ng.manifest: stress-ng.manifest.template
			gramine-manifest \
			-Dlog_level=$(GRAMINE_LOG_LEVEL) \
			-Darch_libdir=$(ARCH_LIBDIR) \
            $< > $@

stress-ng.manifest.sgx: stress-ng.manifest
			gramine-sgx-sign \
			--manifest $< --output $@

stress-ng.sig: stress-ng.manifest.sgx

.PHONY: clean
clean:
		$(RM) *.token *.sig *.manifest.sgx *.manifest pal_loader

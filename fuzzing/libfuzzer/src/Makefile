#ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
ARCH_LIBDIR ?= /lib/x86_64-linux-gnu/

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: libfuzz.manifest
ifeq ($(SGX),1)
all: libfuzz.manifest.sgx libfuzz.sig
endif


libfuzz.manifest: libfuzz.manifest.template
	gramine-manifest \
                -Dlog_level=$(GRAMINE_LOG_LEVEL) \
                -Darch_libdir=$(ARCH_LIBDIR) \
                $< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# see the helloworld example for details on this workaround.
libfuzz.manifest.sgx libfuzz.sig: sgx_sign
        @:

.INTERMEDIATE: sgx_sign
sgx_sign: libfuzz.manifest
	gramine-sgx-sign \
                --manifest $< \
                --output $<.sgx

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: clean
clean:
	$(RM) *.manifest *.manifest.sgx *.token *.sig OUTPUT* *.PID TEST_STDOUT TEST_STDERR
	$(RM) -r scripts/__pycache__

.PHONY: distclean
distclean: clean


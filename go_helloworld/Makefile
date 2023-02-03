ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = trace
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: helloworld helloworld.manifest
ifeq ($(SGX),1)
all: helloworld.manifest.sgx helloworld.sig
endif

helloworld: 
	go build helloworld.go

helloworld.manifest: helloworld.manifest.template
	gramine-manifest \
		-Dlog_level=$(GRAMINE_LOG_LEVEL) \
		$< $@

helloworld.manifest.sgx: helloworld.manifest helloworld
	gramine-sgx-sign \
		--manifest $< \
		--output $@

helloworld.sig: helloworld.manifest.sgx

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: check
check: all
	$(GRAMINE) helloworld > OUTPUT
	echo "Hello, world" | diff OUTPUT -
	@echo "[ Success ]"

.PHONY: clean
clean:
	$(RM) *.token *.sig *.manifest.sgx *.manifest helloworld OUTPUT

.PHONY: distclean
distclean: clean


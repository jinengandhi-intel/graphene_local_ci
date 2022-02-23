.PHONY: all
all: all clean build-release rust-release
ifeq ($(SGX),1)
all: all clean build-release rust-release sign-release get-token-release
endif

PROJNAME=hello

rust-release:
	cargo build --release

target/release/${PROJNAME}.manifest: ${PROJNAME}.manifest.template rust-release
	$(eval EXE_DIR ?= target/release/)
	gramine-manifest -Dlibdir=/lib/x86_64-linux-gnu/ \
					 -Dself_exe=${EXE_DIR}${PROJNAME} \
					 -Dlog_level=error \
					 $< $@

build-release: target/release/${PROJNAME}.manifest


target/release/${PROJNAME}.manifest.sgx: target/release/${PROJNAME}.manifest
	gramine-sgx-sign --manifest $(@D)/$(<F) \
					--output $(@D)/$(<F).sgx \

target/release/${PROJNAME}.sig: target/release/${PROJNAME}.manifest.sgx


sign-release: target/release/${PROJNAME}.sig

target/release/${PROJNAME}.token: target/release/${PROJNAME}.sig
	gramine-sgx-get-token --sig target/release/${PROJNAME}.sig --output target/release/${PROJNAME}.token

get-token-release: target/release/${PROJNAME}.token

run-release-direct: target/release/${PROJNAME}.manifest
	gramine-direct ./target/release/${PROJNAME}

run-release-sgx: get-token-release
	gramine-sgx ./target/release/${PROJNAME}

clean:
	cargo clean


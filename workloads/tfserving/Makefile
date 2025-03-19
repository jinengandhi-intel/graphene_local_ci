ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
CURR_DIR =$(shell pwd)

SERVING=serving

SERVING_HASH=652d6e2caab2b0d8729fe92ed11134222a1ba886d315b113b979155250864950
TFSERVING_HASH=8c96f4398ee19dfd3d3617e615eea251fe5e2e768c8fba83157d10a3dfe1ed7e

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: $(SERVING) tensorflow_model_server.manifest
ifeq ($(SGX),1)
all: tensorflow_model_server.manifest.sgx tensorflow_model_server.sig
endif

ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

$(SERVING):
	../common_tools/download --output $(SERVING).tar.gz --sha256 $(SERVING_HASH) \
     --url https://github.com/tensorflow/serving/archive/refs/tags/2.11.0.tar.gz
	@mkdir $(SERVING)
	tar -C $(SERVING) --strip-components=1 -xzf $(SERVING).tar.gz

tensorflow_model_server.manifest: tensorflow_model_server.manifest.template
	gramine-manifest \
                -Dlog_level=$(GRAMINE_LOG_LEVEL) \
                -Darch_libdir=$(ARCH_LIBDIR) \
                -Dentrypoint=$(realpath $(shell sh -c "command -v tensorflow_model_server")) \
                $< >$@

tensorflow_model_server.manifest.sgx tensorflow_model_server.sig: sgx_sign
        @:

.INTERMEDIATE: sgx_sign
sgx_sign: tensorflow_model_server.manifest | $(SERVING)
	gramine-sgx-sign \
                --manifest $< \
                --output $<.sgx

.PHONY: check
check: all
	$(GRAMINE) tensorflow_model_server --port=8500 --rest_api_port=8501 --tensorflow_intra_op_parallelism=2 --tensorflow_inter_op_parallelism=2 --model_name=half_plus_two --model_base_path=/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu >/dev/null & SERVER_ID=$$!; \
	../../scripts/wait_for_server 2000 127.0.0.1 8501; \
	curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://localhost:8501/v1/models/half_plus_two:predict > OUTPUT; \
	kill -9 $$SERVER_ID
	@grep -q '"predictions": .2.5, 3.0, 4.5' OUTPUT && echo [ "Success" ]
	@rm OUTPUT

.PHONY: run-native
run-native: all
	tensorflow_model_server --port=8500 --rest_api_port=8501 --tensorflow_intra_op_parallelism=2 --tensorflow_inter_op_parallelism=2 --model_name=half_plus_two --model_base_path=$(CURR_DIR)/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu >/dev/null & SERVER_ID=$$!; \
	../../scripts/wait_for_server 60 127.0.0.1 8501; \
	curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://localhost:8501/v1/models/half_plus_two:predict > OUTPUT; \
	kill -9 $$SERVER_ID
	@grep -q '"predictions": .2.5, 3.0, 4.5' OUTPUT && echo [ "Success" ]
	@rm OUTPUT

.PHONY: install-dependencies
install-dependencies:
	../common_tools/download --output tensorflow-model-server_2.18.0_all.deb --sha256 $(TFSERVING_HASH) \
	--url https://storage.googleapis.com/tensorflow-serving-apt/pool/tensorflow-model-server/t/tensorflow-model-server/tensorflow-model-server_2.18.0_all.deb
	sudo dpkg -i ./tensorflow-model-server_2.18.0_all.deb

.PHONY: clean
clean:
	$(RM) tensorflow_model_server.manifest tensorflow_model_server.manifest.sgx tensorflow_model_server.sig OUTPUT

.PHONY: distclean
distclean: clean
	$(RM) -r $(SERVING) $(SERVING).tar.gz

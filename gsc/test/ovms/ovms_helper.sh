mkdir /mnt/tmpfs/model_encrypted

curl --create-dirs https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/face-detection-retail-0004/FP32/face-detection-retail-0004.xml https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/face-detection-retail-0004/FP32/face-detection-retail-0004.bin -o models/1/face-detection-retail-0004.xml -o models/1/face-detection-retail-0004.bin
gramine-sgx-pf-crypt encrypt -w test/pytorch/base_image_helper/encryption_key -i models -o /mnt/tmpfs/model_encrypted/

docker build --tag ovms-image --file test/ovms/ovms-gsc.dockerfile test/ovms/

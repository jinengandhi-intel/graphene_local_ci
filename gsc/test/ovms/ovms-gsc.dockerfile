# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2023 Intel Corporation

# This template is used by `curation_script.sh` to create a wrapper dockerfile
# `openvino-model-server-gsc.dockerfile` that includes user provided inputs e.g. `ca.cert` file
# etc. into the graminized OpenVINO Model Server image.

# The curation script fills the <base_image_name> during curation.
FROM openvino/model_server:2023.0

# Below line copies cert files into the image if user selects remote attestation
#COPY ca.crt /
CMD ["--model_path", "/mnt/tmpfs/model_encrypted", "--model_name", "face-detection", "--port", "9000", "--shape", "auto"]

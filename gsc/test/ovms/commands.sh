curl https://raw.githubusercontent.com/openvinotoolkit/model_server/releases/2023/0/demos/common/python/client_utils.py -o test/ovms/client_utils.py
curl https://raw.githubusercontent.com/openvinotoolkit/model_server/releases/2023/0/demos/face_detection/python/face_detection.py -o test/ovms/face_detection.py
curl --create-dirs https://raw.githubusercontent.com/openvinotoolkit/model_server/releases/2023/0/demos/common/static/images/people/people1.jpeg -o test/ovms/images/people1.jpeg
mkdir test/ovms/results
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r test/ovms/client_requirements.txt
export no_proxy=intel.com,.intel.com,localhost,127.0.0.1
python3 test/ovms/face_detection.py --batch_size 1 --width 600 --height 400 --input_images_dir test/ovms/images --output_dir test/ovms/results --grpc_port 9000
deactivate
file_to_check="test/ovms/results/1_0.jpg"
output_file="test/ovms/ovms_result.txt"
if [ -f "$file_to_check" ]; then
    echo "SUCCESS : File exists." > "$output_file"
else
    echo "ERROR : File does not exist." > "$output_file"
fi

import argparse
import os
import glob
import sys

def main():
    error_files_list = []
    parser = argparse.ArgumentParser(description='Stress-ng Result Parser')
    parser.add_argument('--path', help='File Log Path')
    args = parser.parse_args()

    if args.path:
        log_path = args.path
    else:
        log_path = os.getcwd()
    
    log_files = glob.glob(log_path + "/*.log")

    for files in log_files:
        fd = open(files, 'r')
        error_in_file = False
        for line in fd.readlines():
            if ("error" in line) and ("Using insecure argv source" not in line) and ("Gramine will continue application execution" not in line):
                error_in_file = True
    
        if error_in_file:
            error_files_list.append(files)

    print(error_files_list)    
    if len(error_files_list) > 0:
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

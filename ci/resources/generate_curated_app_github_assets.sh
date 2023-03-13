#!/bin/bash


BUILD_ALL_WORKLOAD=0
BUILD_REDIS_WORKLOAD=0
BUILD_PYTORCH_WORKLOAD=0
BUILD_TFSERVING_WORKLOAD=0
BUILD_SKLEARN_WORKLOAD=0
WORKSPACE=`pwd`
RELEASE_TAG=""

workload_list=''

function usage()
{
 echo -e "Usage:
        eg : $0 -tag 1.4 -redis -pytorch [clones contrib repo from 1.4 tag and creates assets for redis pytorch]
        eg : $0 -tag 1.3 -all [clones contrib repo from 1.3 tag and creates assets for all the workload supported]
        $0 <OPTION>\n
        OPTION:
           [-tag 1.4: clones contrib repo from the mentioned tag][MUST]
           [-all: Generate Github Assets for all the workload]
           [-redis: Generate Github Release for redis]
           [-pytorch: Generate Github Release for pytorch]
           [-tfserving: Generate Github Release for tf-serving]
           [-sklearn: Generate Github Release for sklearn]
           [-redis -pytorch: Generate Github Assets for redis and pytorch]"
}

function parse_args()
{
  i=1
  total_args=$#
  if [ $total_args -eq 0 ]; then
    echo "No arguments provided"
    usage;
    exit 1
  fi
  while [ $i -le $total_args ]; do
    i=$((i+1))
    case "$1" in
      -tag)
        RELEASE_TAG=$2
        i=$((i+1))
        shift 2;;
      -all)
        BUILD_ALL_WORKLOAD=1
        shift;;
      -redis)
        BUILD_REDIS_WORKLOAD=1
        shift;;
      -pytorch)
        BUILD_PYTORCH_WORKLOAD=1
        shift;;
      -tfserving)
        BUILD_TFSERVING_WORKLOAD=1
        shift;;
      -sklearn)
        BUILD_SKLEARN_WORKLOAD=1
        shift;;
      -help)
        usage;
        exit 1
        ;;
        *)
        echo "improper usage of arguments"
        usage;
        exit 1
    esac
  done
}

function add_workload()
{
  if [ -z "$workload_list" ]; then
    workload_list="$1"
  else
    workload_list="${workload_list} $1"
  fi
}

function init()
{
  # clone contrib repo
  [[ -d contrib ]] && rm -rf contrib
  git clone https://github.com/gramineproject/contrib.git -b $RELEASE_TAG

  if [ $BUILD_ALL_WORKLOAD -eq 1 ]; then
    cd contrib/Curated-Apps/workloads
    workload_list=`ls -d */ | cut -f1 -d'/'`
    cd $WORKSPACE
  else 
    if [ $BUILD_REDIS_WORKLOAD -eq 1 ]; then
      add_workload "redis"
    fi
    if [ $BUILD_PYTORCH_WORKLOAD -eq 1 ]; then
      add_workload "pytorch"
    fi
    if [ $BUILD_TFSERVING_WORKLOAD -eq 1 ]; then
      add_workload "tensorflow-serving"
    fi
    if [ $BUILD_SKLEARN_WORKLOAD -eq 1 ]; then
      add_workload "sklearn"
    fi
  fi

}

function generate_release_assets()
{
  for workload in $workload_list
  do
    echo $workload
    workload_dir=curated_app_${RELEASE_TAG}_${workload}
    [[ -d ${workload_dir} ]] && rm -rf ${workload_dir}
    echo "creating ${workload_dir}....."
    mkdir ${workload_dir}
    cp -rf contrib/Curated-Apps/* ${workload_dir}
    cd ${workload_dir}/workloads/
    find . ! -name ${workload} -type d -maxdepth 1 -mindepth 1 -exec rm -rv {} +
    cd ..
    find . -name '.gitignore' -type f -exec rm -rv {} +
    cd $WORKSPACE
    tar -czvf ${workload_dir}.tar.gz ${workload_dir}/
    rm -rf ${workload_dir}
  done

}

parse_args "$@"
init
echo "workloads selected to generate release assets : $workload_list"
generate_release_assets 






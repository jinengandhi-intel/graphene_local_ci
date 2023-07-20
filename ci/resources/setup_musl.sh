#!/bin/bash
set -x

cd $WORKSPACE/gramine/CI-Examples
if [[ "$base_os" != *"alpine"* ]]; then
  arch_lib="\/lib"
else
  arch_lib="\/usr\/local\/lib"
fi

for i in $(find -name '*manifest.template');
do
  sed -i 's/{ path = "\/lib", uri = "file:{{ gramine.runtimedir() }}/{ path = "'$arch_lib'", uri = "file:{{ gramine.runtimedir(libc='\''musl'\'') }}/' $i;
  sed -i 's/{ uri = "file:{{ gramine.runtimedir() }}", path = "\/lib"/{ uri = "file:{{ gramine.runtimedir(libc='\''musl'\'') }}", path = "'$arch_lib'"/' $i;
  sed -i 's/{ path = "\/gramine_lib", uri = "file:{{ gramine.runtimedir() }}/{ path = "\/gramine_lib", uri = "file:{{ gramine.runtimedir(libc='\''musl'\'') }}/' $i;
  sed -i 's/^\s*"file:{{ gramine.runtimedir() /  "file:{{ gramine.runtimedir(libc='\''musl'\'') /' $i;
  if [[ "$base_os" == *"alpine"* ]]; then
    sed -i 's/loader.env.LD_LIBRARY_PATH = "\/lib/loader.env.LD_LIBRARY_PATH = "\/usr\/local\/lib/' $i;
  fi
done;


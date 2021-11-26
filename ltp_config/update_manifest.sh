#!/bin/bash

if [[ $LTPSCENARIO == *"syscalls-new"* ]]; then
    sed 's/allowed_files = \[/&"file:pipe2_02_child",/' $PWD/pipe2_02.manifest
    sed 's/allowed_files = \[/&"file:execvp01_child",/' $PWD/execvp01.manifest
    sed 's/allowed_files = \[/&"file:execv01_child",/' $PWD/execv01.manifest
    sed 's/allowed_files = \[/&"file:execlp01_child",/' $PWD/execlp01.manifest
    sed 's/allowed_files = \[/&"file:execl01_child",/' $PWD/execl01.manifest
fi
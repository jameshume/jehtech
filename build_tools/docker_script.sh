#!/bin/bash

function estimate_num_build_cores()
{
    local NUM_MAKE_PROCESSES
    NUM_MAKE_PROCESSES=$(lscpu | grep "^\s*CPU(s):" | sed 's/.*:\s*//g')
    if [ -z "$NUM_MAKE_PROCESSES" ]
    then
        echo "WARNING: Failed to estimate #cores. Setting to 1 core."
        NUM_MAKE_PROCESSES=1
    fi
    echo "$NUM_MAKE_PROCESSES"
}

cd /jehtech/build_tools
make -j"$(estimate_num_build_cores)" all > /jehtech/docker_deploy_output.txt

if [ "$1" == "DEPLOY" ]
then
    echo "DOing the deploy" >> /jehtech/docker_deploy_output.txt
    make deploy >> /jehtech/docker_deploy_output.txt
fi
#!/bin/bash

function estimate_num_build_cores()
{
    local NUM_MAKE_PROCESSES
    NUM_MAKE_PROCESSES=$(lscpu | grep "^\s*CPU(s):" | sed 's/.*:\s*//g')
    if [ -z "$NUM_MAKE_PROCESSES" ]
    then
        echo "WARNING: Failed to estimate #cores. Setting to 1 core." > /proc/1/fd/1
        NUM_MAKE_PROCESSES=1
    fi
    echo "$NUM_MAKE_PROCESSES"
}

cd /jehtech/build_tools
make -j"$(estimate_num_build_cores)" all > /proc/1/fd/1

if [ "$1" == "DEPLOY" ]
then
    echo "DOing the deploy" > /proc/1/fd/1
    make deploy > /proc/1/fd/1
fi
#!/bin/bash
cd /home/inflowsense/repos/jehtech/projects_not_in_own_repo/gcalander_notifier
source .venv/bin/activate
while true
do
    python3 main.py
    sleep 1m
done
deactivate
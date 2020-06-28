#!/bin/bash
# See https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html
# sudo apt install awscli
aws s3 sync __deployed s3://jehtech.com

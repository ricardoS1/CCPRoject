#!/bin/bash

aws cloudformation create-stack \
	--stack-name group1Project \
	--template-body file://$PWD/p1.yml \
	--capabilities CAPABILITY_NAMED_IAM

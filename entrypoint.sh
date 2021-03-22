#!/bin/sh

PARAMS_STRING=""

# ARG- Must Supply Suppressions File Path 
if [ ! -z "$1" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$1"
fi

# ARG - Trivy Report Path Argument
if [ ! -z "$2" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$2"
fi

# ARG - Create Github Issues Bool
if [ ! -z "$3" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$3"
fi

# ARG - Minimum Severity to create GH issues
if [ ! -z "$4" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$4"
fi

# ARG - Create Slack Notifications Bool
if [ ! -z "$5" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$5"
fi

# ARG - Minimum Severity to create Slack alerts
if [ ! -z "$6" ]
then
	PARAMS_STRING = "${PARAMS_STRING} --report-path=$6"
fi

echo "$PARAMS_STRING"
 
python3 trivy_json_report_parse.py --report-path="trivy_report.json" 
#python3 trivy_json_report_parse.py $PARAMS_STRING 

#!/bin/sh

PARAMS_STRING=""

# ARG- Must Supply Trivy Report Path 
if [ ! -z "$1" ]
then
	PARAMS_STRING+="--report-path=$1"
fi

# ARG - Trivy Suppressions List File Path
if [ ! -z "$2" ]
then
	PARAMS_STRING+="--suppressions-path=$2"
fi

# ARG - Create Github Issues Bool
if [ ! -z "$3" ]
then
	PARAMS_STRING+="--github=$3"
fi

# ARG - Minimum Severity to create GH issues
if [ ! -z "$4" ]
then
	PARAMS_STRING+="--minSeverityGithub=$4"
fi

# ARG - Create Slack Notifications Bool
if [ ! -z "$5" ]
then
	PARAMS_STRING+="--slack=$5"
fi

# ARG - Minimum Severity to create Slack alerts
if [ ! -z "$6" ]
then
	PARAMS_STRING+="--minSeveritySlack=$6"
fi

echo "$PARAMS_STRING"
 
#python3 trivy_json_report_parse.py --report-path="trivy_report.json" 
python3 trivy_json_report_parse.py $PARAMS_STRING 

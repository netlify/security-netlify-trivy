#!/usr/bin/env python3

import json
import requests
import argparse
import codecs
import subprocess
import os
import hashlib
import time
import glob
from slack import WebClient
from slack.errors import SlackApiError
from github import Github

def parse_report_for_issues(slack_webhook, slack_alert, github_issue, slack_severity, github_severity):
    filename = 'trivy_report.json' 
    with open(filename, 'r+') as json_file:
        json_data = json.load(json_file)
        for target in json_data:
#            print("Entire Target: {}\n".format(target))
            for vulnerability in target['Vulnerabilities']:
#                print("Vulnerability: {}\n".format(vulnerability))
                issue_title = "container image vulnerability - " + json.dumps(vulnerability['PkgName']) + " - " + json.dumps(vulnerability['InstalledVersion'])
                message = "**New Finding Alert**\n"
                if 'Title' in vulnerability:
                    message += "**Title**: " + json.dumps(vulnerability['Title']) + "\n"
                message += "**Package Name**: " + json.dumps(vulnerability['PkgName']) + "\n"
                message += "**Severity**: " + json.dumps(vulnerability['Severity']) + "\n"
                message += "**Installed Version**: " + json.dumps(vulnerability['InstalledVersion']) + "\n"
                message += "**Description**: " + json.dumps(vulnerability['Description']) + "\n"
                message += "**Layer SHA256**: " + json.dumps(vulnerability['Layer']['DiffID']) + "\n"
                message += "**Primary URL**: " + json.dumps(vulnerability['PrimaryURL']) + "\n"
                if 'CVSS' in vulnerability:
                    message += "**CVSS Score**: " + json.dumps(vulnerability['CVSS']) + "\n"
                message += "**References**: " + json.dumps(vulnerability['References']) + "\n"
                if 'PublishedDate' in vulnerability:
                    message += "**Published Date**: " + json.dumps(vulnerability['PublishedDate']) + "\n"
                if 'LastModifiedDate' in vulnerability:
                    message += "**Last Modified Date**: " + json.dumps(vulnerability['LastModifiedDate']) + "\n"
                    fixable = "true"
                print(message + "\n")

                # Checking if sha256 is in suppressions file
                file = open('.github/workflows/trivy-files/suppressions-trivy', 'r')
                file_lines = file.readlines()
                count = 0
                suppression_match = "false"
                for line in file_lines:
                    #print("Line{}: {}".format(count, line.strip().split(' ', 1)[0]))
                    if json.dumps(vulnerability['Layer']['DiffID']).strip('\"') == line.strip().split(' ', 1)[0]:
                        suppression_match = "true"

                #If not suppressed, and there is a fix available, send to slack and or create gh issue
                if suppression_match == "false" and fixable == "true":
                    if slack_alert == "true":
                        for sev_level in slack_severity:
                            if json.dumps(vulnerability['Severity']) == sev_level: 
                                send_slack_alert(slack_webhook, message)
                    if github_issue == "true":
                        for sev_level in github_severity:
                            if json.dumps(vulnerability['Severity']) == sev_level: 
                                dedup_and_create_gh_issue(message, issue_title, json.dumps(vulnerability['Severity']).strip('\"'))
    #except:
        #print(" [ERROR] Cannot open file: " + filename)

def get_slack_webhook_from_env() -> str:
    slack_webhook=os.environ.get('CONTAINER_SCAN_SLACK_WEBHOOK', None) 
    if slack_webhook is None:
        raise ValueError(
            'Must provide slack_webhook.'
        )
    return slack_webhook

def get_gh_access_token_from_env() -> str:
    gh_access_token=os.environ.get('CONTAINER_SCAN_GH_ACCESS_TOKEN', None)
    if gh_access_token is None:
        raise ValueError(
            'Must provide github_access_token.'
        )
    return gh_access_token

def get_repo_from_env() -> str:
    repo_path = os.environ.get('GITHUB_REPO', None)
    if repo_path is None:
        raise ValueError(
               'Must provide repo.',
               'eg. netlify/containerscan' 
        )
    return repo_path

def matches_issue_in_repo(repo_path, g, issue_title):
    issues = get_issues_from_repo(repo_path, g)
    for issue in issues:
        print(f"Issue : {issue} \n")
        print(f"Issue : {issue.title} \n")
        if issue.title == issue_title:
            print("Issue " + issue.title + " already exists\n")
            issue_matched = "true"
            return issue_matched
        
def get_issues_from_repo(repo_path, g):
    repo = g.get_repo(repo_path)
    return repo.get_issues()

def dedup_and_create_gh_issue(message, issue_title, severity):
    repo_path = get_repo_from_env()
    print("Repo Path: " + repo_path + "\n")
    gh_access_token = get_gh_access_token_from_env()
    g = Github(gh_access_token)
    issue_matched = matches_issue_in_repo(repo_path, g, issue_title)
    if issue_matched != "true":
        create_gh_issue(message, issue_title, repo_path, g, severity)

def create_gh_issue(message, issue_title, repo_path, g, severity):
    repo = g.get_repo(repo_path)
    i = repo.create_issue(
        title=issue_title,
        body=message,
        labels=[
             "security", 
             "security-risk: " + severity,
             "trivy"
        ]
    )

def send_slack_alert(slack_webhook, message):
    data = {
        'text': message,
        'username': 'Container-Scan-Bot',
        'icon_emoji': ':boar:'
    }

    response = requests.post(slack_webhook, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

def main():
#    file = open('/tmp/git-credentials', 'r')
#    file_lines = file.readlines()
#    for line in file_lines:
#        print(line)    

    slack_webhook = "Null"
    slack_alert = "false"
    github_issue = "false" 

    parser = argparse.ArgumentParser(description="Trivy Container Scanner")
    parser.add_argument('-g',"--github",required=False,default=False,help="Create a Github Issue for Each Vulnerability")
    parser.add_argument('-s',"--slack",required=False,default=False,help="Send a Slack Alert for Each Vulnerability")
    parser.add_argument('-k',"--minSeveritySlack",required=False,default="low",help="Minimum Severity for Alerting Slack eg. critical,high,medium,low")
    parser.add_argument('-b',"--minSeverityGithub",required=False,default="low",help="Minimum Severity for Creating Github Issue eg. critical,high,medium,low")
    args = parser.parse_args()
    if args.slack == "True" or args.slack == "true" or args.slack == "T" or args.slack == "t":
        slack_alert = "true"
    if args.github == "True" or args.github == "true" or args.github == "T" or args.github == "t":
        github_issue = "true"

    if args.minSeveritySlack == "Critical" or args.minSeveritySlack == "critical" or args.minSeveritySlack == "C" or args.minSeveritySlack == "c":
        slack_severity = ['"CRITICAL"']
    elif args.minSeveritySlack == "High" or args.minSeveritySlack == "high" or args.minSeveritySlack == "H" or args.minSeveritySlack == "h":
        slack_severity = ['"CRITICAL"', '"HIGH"']
    elif args.minSeveritySlack == "Medium" or args.minSeveritySlack == "medium" or args.minSeveritySlack == "M" or args.minSeveritySlack == "m":
        slack_severity = ['"CRITICAL"', '"HIGH"', '"MEDIUM"']
    else: slack_severity = ['"CRITICAL"', '"HIGH"', '"MEDIUM"', '"LOW"']
    
    if args.minSeverityGithub == "Critical" or args.minSeverityGithub == "critical" or args.minSeverityGithub == "C" or args.minSeverityGithub == "c":
        github_severity = ['"CRITICAL"']
    elif args.minSeverityGithub == "High" or args.minSeverityGithub == "high" or args.minSeverityGithub == "H" or args.minSeverityGithub == "h":
        github_severity = ['"CRITICAL"', '"HIGH"']
    elif args.minSeverityGithub == "Medium" or args.minSeverityGithub == "medium" or args.minSeverityGithub == "M" or args.minSeverityGithub == "m":
        github_severity = ['"CRITICAL"', '"HIGH"', '"MEDIUM"']
    else: github_severity = ['"CRITICAL"', '"HIGH"', '"MEDIUM"', '"LOW"']

    if slack_alert == "true":
        slack_webhook = get_slack_webhook_from_env()


    message = "Starting Trivy Report Parse\n"
    print(message)
    if slack_alert == "true":
        send_slack_alert(slack_webhook, message)

    parse_report_for_issues(slack_webhook, slack_alert, github_issue, slack_severity, github_severity)

    message = "Trivy Report Parse Completed!\n"
    print(message)
    if slack_alert == "true":
        send_slack_alert(slack_webhook, message)

if __name__ == "__main__":
    main()

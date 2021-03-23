# Security Netlify Trivy Parse
[Trivy is a container scanning tool from aquasecurity](https://github.com/aquasecurity/trivy). This action is written in python and parses the trivy report to provide extra functionality, such as, suppression handling, alerting to slack, opening github issues with labels specifying risk level, by specifying which severity levels of notifications. This tool is meant to work automatically after using `aquasecurity/trivy-action@master`, which will pick up `Dockerfile` in the root level of a repo. 

## Inputs

#### `trivy_report_file_path`

**Required** - location of trivy report that will be parsed

#### `suppression_file_path` 

path/name of suppression list file
Sometimes a particular vulnerability does not need to be addressed. This can be due to the environment or other priority directives. To suppress the vulnerability from the alerted findings, add the contents of the `Layer SHA256` value to a `suppressions` file, and indicate the path as an input. 

#### `create_github_issue`

boolean if user wishes to create github issues

#### `github_min_severity`

issues will be created for all discovered vulnerabilities with >= this severity
You can specify the severity of issues created by specifying Critical, High, Medium or Low. It is important to understand that this will create issues for all findings greater than and including the chosen severity level.  The default is `Low`

#### `create_slack_notification` 

boolean if user wishes to create slack alert

#### `slack_min_severity`

alerts will be sent to slack for all discovered vulnerabilities with >= severity
You can specify the slack alert severity by specifying Critical, High, Medium or Low.It is important to understand that you will recieve alerts for all findings greater than and including the chosen severity level.  The default is `Low`.

#### `container_scan_slack_webhook` 

container_scan_slack_webhook: ${{ secrets.CONTAINER_SCAN_SLACK_WEBHOOK }}

#### `container_scan_gh_access_toke`         

container_scan_gh_access_token: ${{ secrets.GITHUB_TOKEN }}

####  `github_repo_name`

github_repo_name: ${{ github.repository}}


## Example Usage 
First you must call the trivy action or get trivy directly and use it:

```
```

or

```
      - name: Get Trivy
        run: curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b ~

      - name: Trivy Container Scan
        run: /home/runner/trivy image -f json -o trivy_report.json --skip-dirs "usr/local/bundle/ruby, /usr/local/bundle/ruby" trivy-ci-test:latest
```




```
      - name: Trivy Parse Report
        uses: netlify/security-netlify-trivy@v0.3
        with:
          trivy_report_file_path: 'trivy_report.json'
          suppression_file_path: 'suppressions'
          create_github_issue: 'true'
          github_min_severity: 'high'
          create_slack_notification: 'false'
          slack_min_severity: 'critical'
          container_scan_slack_webhook: ${{ secrets.CONTAINER_SCAN_SLACK_WEBHOOK }}
          container_scan_gh_access_token: ${{ secrets.GITHUB_TOKEN }}
          github_repo_name: ${{ github.repository}}
```


### Alerting to Slack
This tool can alert to slack. By specifying `-s/--slack=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will send an alert to slack for each finding. The default is `false`.

You can specify the slack alert severity by specifying Critical, High, Medium or Low using `-k/--minSeveritySlack=Low` argument in the python execution in the workflow file. It is important to understand that you will recieve alerts for all findings greater than and including the chosen severity level.  The default is `Low`.

You must also call an input `CONTAINER_SCAN_SLACK_WEBHOOK` in the workflow file, and populate it by using github secrets.

### Creating Github Issues
This tool can create issues in github. By specifying `-g/--github=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will create a github issue for each finding. The default is `false`.

You can specify the severity of issues created by specifying Critical, High, Medium or Low using `-k/--minSeverityGithub=Low` argument in the python execution in the workflow file. It is important to understand that this will create issues for all findings greater than and including the chosen severity level.  The default is `Low`

You must also call a inut `CONTAINER_SCAN_GH_ACCESS_TOKEN` in the workflow file, and populate it by using github secrets.

### Suppressions

### Docker build arguments
If your Container Image requires build arguments, you can add those to the GH Action workflow as necessary, using GH secrets where necessary.

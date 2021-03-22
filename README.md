# Security Netlify Trivy Parse
[Trivy is a container scanning tool from aquasecurity](https://github.com/aquasecurity/trivy). This action is written in python and pareses the trivy report to provide extra functionality, such as, suppression handling, alerting to slack, opening github issues with labels specifying risk level, by specifying which severity levels of notifications. This tool is meant to work automatically with `action/trivy` to pick up `Dockerfile` in the root level of a repo. 

## Inputs

### `trivy_report_file_path`

**Required** - location of trivy report that will be parsed

### `suppression_file_path` 

path/name of suppression list file

### `create_github_issue`

boolean if user wishes to create github issues

### `github_min_severity`

issues will be created for all discovered vulnerabilities with >= this severity
You can specify the severity of issues created by specifying Critical, High, Medium or Low using `-k/--minSeverityGithub=Low` argument in the python execution in the workflow file. It is important to understand that this will create issues for all findings greater than and including the chosen severity level.  The default is `Low`

### `create_slack_notification` 

boolean if user wishes to create slack alert

### `slack_min_severity`

alerts will be sent to slack for all discovered vulnerabilities with >= severity
You can specify the slack alert severity by specifying Critical, High, Medium or Low using `-k/--minSeveritySlack=Low` argument in the python execution in the workflow file. It is important to understand that you will recieve alerts for all findings greater than and including the chosen severity level.  The default is `Low`.


### ENV Vars
Must use ENV names as specified:
```
  env:
    - CONTAINER_SCAN_SLACK_WEBHOOK: ${{ secrets.CONTAINER_SCAN_SLACK_WEBHOOK }}
    - CONTAINER_SCAN_GH_ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    - GITHUB_REPO: ${{ github.repository}}`
```

## Example Usage 

```
uses: actions/name
with: 
  trivy_report_file_path: 'trivy_report.json'
  suppression_file_path: 'suppressions-trivy'
  create_github_issue: 'true'
  github_min_severity: 'high'
  create_slack_notification: 'true'
  slack_min_severity: 'critical'
env:
  CONTAINER_SCAN_SLACK_WEBHOOK: ${{ secrets.CONTAINER_SCAN_SLACK_WEBHOOK }}
  CONTAINER_SCAN_GH_ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  GITHUB_REPO: ${{ github.repository}}
```



## Older Verbiage

### Building from GCR images

This tool is capable of pulling images from GCR automatically by pulling org level secrets.
Bur you can use any GCP Access Token with enough privelege, simply uncomment the ENVVAR called `GC_API_CREDS` in the workflow file, and populate it by using github secrets. 

Pro-tip: One easy way to obtain a 60 min lifetime token for testing is by using `gcloud auth print-access-token` while logged in to GCP. 

### Alerting to Slack
This tool can alert to slack. By specifying `-s/--slack=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will send an alert to slack for each finding. The default is `false`.

You can specify the slack alert severity by specifying Critical, High, Medium or Low using `-k/--minSeveritySlack=Low` argument in the python execution in the workflow file. It is important to understand that you will recieve alerts for all findings greater than and including the chosen severity level.  The default is `Low`.

You must also uncomment the ENVVAR called `CONTAINER_SCAN_SLACK_WEBHOOK` in the workflow file, and populate it by using github secrets.

### Creating Github Issues
This tool can create issues in github. By specifying `-g/--github=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will create a github issue for each finding. The default is `false`.

You can specify the severity of issues created by specifying Critical, High, Medium or Low using `-k/--minSeverityGithub=Low` argument in the python execution in the workflow file. It is important to understand that this will create issues for all findings greater than and including the chosen severity level.  The default is `Low`

You must also uncomment the ENVVAR called `CONTAINER_SCAN_GH_ACCESS_TOKEN` in the workflow file, and populate it by using github secrets.

### Suppressions
Sometimes a particular vulnerability does not need to be addressed. This can be due to the environment or other priority directives. To suppress the vulnerability from the alerted findings, add the contents of the `Layer SHA256` value to the `suppressions` file. 

### Docker build arguments
If your Container Image requires build arguments, you can add those to the GH Action workflow as necessary, using GH secrets where possible
Example: `run: docker build --build-arg BUNDLE_ENTERPRISE__CONTRIBSYS__COM=${{ secrets.SIDEKIQ_ENT_ACCESS_KEY }} -t trivy-ci-test:latest .`

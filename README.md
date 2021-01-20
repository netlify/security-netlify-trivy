# Trivy Container Scan Action
[Trivy is a container scanning tool from aquasecurity](https://github.com/aquasecurity/trivy). This action is written in python and wraps trivy to provide extra functionality, such as, suppression handling, alerting to slack, opening github issues, and specifying severity levels of notifications. This tool will automatically pick up `Dockerfile` in the root level of a repo. 

### Building from GCR images
This tool is capable of pulling images from GCR. Simply uncomment the ENVVAR called `GC_API_CREDS` in the workflow file, and populate it by using github secrets. 

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


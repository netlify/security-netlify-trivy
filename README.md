# Security Netlify Trivy Parse
[Trivy is a container scanning tool from aquasecurity](https://github.com/aquasecurity/trivy). This action is written in python and parses the trivy report to provide extra functionality, such as, suppression handling, alerting to slack, opening github issues with labels specifying risk level, by specifying which severity levels of notifications. This tool is meant to work automatically after using `aquasecurity/trivy-action@master`, which will pick up all files that start with `Dockerfile*` in the root level of a repo. 

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

#### `container_scan_gh_access_token`         

container_scan_gh_access_token: ${{ secrets.GITHUB_TOKEN }}

####  `github_repo_name`

github_repo_name: ${{ github.repository}}

### Docker build arguments
If your Container Image requires build arguments, you can add those to the build step of GH Action workflow as necessary, using env vars if you need.
Right now this is pretty cloogy using case statements but here is an example=

```
      - name: Processing found Dockerfiles from output, building images
        id: build-image
        run: |
          TEMP_REPORT_NAME="$(echo "${{ matrix.filelist }}" | tr "[A-Z]" "[a-z]" | sed 's/\./-/g')"
          echo $TEMP_REPORT_NAME
          echo "::set-output name=TEMPREPORTNAME::$TEMP_REPORT_NAME"
          if [[ ${{ matrix.filelist }} == Dockerfile.ubuntu18-ruby ]]; then
              docker build --build-arg=RUBY_VERSION=$RUBY_VERSION -t image-$TEMP_REPORT_NAME:latest -f ${{ matrix.filelist }} .
          else
              docker build -t image-$TEMP_REPORT_NAME:latest -f ${{ matrix.filelist }} .
          fi
        env:
          RUBY_VERSION: '3.0.0'
```


## Example Usage
See [Example Workflow](https://github.com/netlify/security-netlify-trivy/blob/main/workflow.yml)

## Manually running the python script on your trivy report

### Alerting to Slack
This tool can alert to slack. By specifying `-s/--slack=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will send an alert to slack for each finding. The default is `false`.

You can specify the slack alert severity by specifying Critical, High, Medium or Low using `-k/--minSeveritySlack=Low` argument in the python execution in the workflow file. It is important to understand that you will recieve alerts for all findings greater than and including the chosen severity level.  The default is `Low`.

You must also have envvar `CONTAINER_SCAN_SLACK_WEBHOOK`

### Creating Github Issues
This tool can create issues in github. By specifying `-g/--github=true` as an argument in `.github/workflows/trivy-main.yml` python trivy execution, it will create a github issue for each finding. The default is `false`.

You can specify the severity of issues created by specifying Critical, High, Medium or Low using `-k/--minSeverityGithub=Low` argument in the python execution in the workflow file. It is important to understand that this will create issues for all findings greater than and including the chosen severity level.  The default is `Low`

You must also have envvar `CONTAINER_SCAN_GH_ACCESS_TOKEN` 

### Ignoring Specific Dockerfiles
You can add the following line after the TEMPLIST variable is defined as shown in the example. Do this for each Dockerfile you wish to have completely ignored.

```
        # Modify the following line to ignore specific Dockerfiles
        IGNORELIST=("Dockerfile.ignore-me")
        TEMPLIST="$(awk '{ printf "\"%s\"\n", $0 }' <(comm -23 <(ls -1 *Dockerfile*) <(printf '%s\n' "${IGNORELIST[@]}" )) | paste -s -d, - | sed 's/,/, /g' | sed 's/^/[ /;s/$/ ]/')"
        echo $TEMPLIST
        echo "::set-output name=matrix::$TEMPLIST"
```

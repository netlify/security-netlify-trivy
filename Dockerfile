
FROM ubuntu:18.04

WORKDIR /

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3" "trivy_json_report_parse.py --github=true --slack=false --minSeverityGithub=h"]


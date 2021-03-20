
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]
ENTRYPOINT ["sh", "-c", "python3 trivy_json_report_parse.py --github=false --slack=false"]


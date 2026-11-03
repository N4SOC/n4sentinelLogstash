FROM docker.elastic.co/logstash/logstash:9.5.6-amd64

ARG environment_name 

RUN logstash-plugin install microsoft-sentinel-log-analytics-logstash-output-plugin

RUN rm -f /usr/share/logstash/pipeline/*
RUN rm -f /usr/share/logstash/config/logstash.yml
RUN rm -f /usr/share/logstash/config/pipeslines.yml

COPY pipeline/ /usr/share/logstash/pipeline/
COPY config/ /usr/share/logstash/config/

RUN sed -i "s|<environment_name>|${environment_name}|g" /usr/share/logstash/pipeline/sentinel.conf 

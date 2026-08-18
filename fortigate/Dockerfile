FROM docker.elastic.co/logstash/logstash:9.5.1-amd64

ARG environment_name 
ARG appId 
ARG appSecret 
ARG tenantId 
ARG dce 
ARG dcrId 
ARG table

RUN logstash-plugin install microsoft-sentinel-log-analytics-logstash-output-plugin

RUN rm -f /usr/share/logstash/pipeline/*
RUN rm -f /usr/share/logstash/config/logstash.yml
RUN rm -f /usr/share/logstash/config/pipeslines.yml

COPY pipeline/ /usr/share/logstash/pipeline/
COPY config/ /usr/share/logstash/config/

RUN sed -i "s|<environment_name>|${environment_name}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<appId>|${appId}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<appSecret>|${appSecret}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<tenantId>|${tenantId}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<dce>|${dce}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<dcrId>|${dcrId}|g" /usr/share/logstash/pipeline/sentinel.conf 
RUN sed -i "s|<table>|${table}|g" /usr/share/logstash/pipeline/sentinel.conf 


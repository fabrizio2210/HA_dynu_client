FROM debian
MAINTAINER fabrizio2210


RUN apt-get update && apt-get install -y python2.7 python-requests curl && apt-get clean

COPY src/* /usr/local/bin/



CMD /usr/local/bin/keep_updated_record.py

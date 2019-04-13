FROM balenalib/armv7hf-debian
MAINTAINER fabrizio2210

RUN [ "cross-build-start" ]

RUN apt-get update && apt-get install -y python2.7 python-requests && apt-get clean

#COPY src/keep_updated_record.py /usr/local/bin/
#COPY src/isItAlive.sh /usr/local/bin
#COPY src/isIt200.sh /usr/local/bin
COPY src/* /usr/local/bin/

RUN [ "cross-build-end" ]

CMD /usr/local/bin/keep_updated_record.py

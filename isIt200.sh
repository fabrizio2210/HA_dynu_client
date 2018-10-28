#!/bin/bash

# Test if a site answers 200 OK
# Verify if an arbitrary page answers 200 OK

[ ! -z "$DYNU_DEBUG" ] && set -x

IP='localhost'
port='80'
virtualHost='none'
secure='0'
page=''

while getopts ":v:i:p:s:l:" opt; do
  case $opt in
    v)
      virtualHost=$(echo $OPTARG | tr -d '[[:space:]]')
      ;;
		i)
			IP=$(echo $OPTARG | tr -d '[[:space:]]')
			;;
		p)
			port=$(echo $OPTARG | tr -d '[[:space:]]')
			;;
		s)
			secure=$(echo $OPTARG | tr -d '[[:space:]]')
      ;;
		l)
			page=$(echo $OPTARG | tr -d '[[:space:]]')
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ $secure == '1' ] ; then
  s='s'
fi
response=$(curl --connect-timeout 10 -sL --resolve "$virtualHost:$port:$IP" -w "%{http_code}\\n" http$s://$virtualHost:$port/$page -o /dev/null)
if [ $response ==  '200' ] ; then
  exit 0
else
  exit 1
fi


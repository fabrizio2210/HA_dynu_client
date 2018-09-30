#!/bin/bash

#  Test if a site has the alive page
# A page with a word "alive" is expected in path "alive.html"

[ ! -z "$DYNU_DEBUG" ] && set -x

IP='localhost'
port='80'
virtualHost='none'
secure='0'

while getopts ":v:i:p:s:" opt; do
  case $opt in
    v)
      virtualHost=$OPTARG
      ;;
		i)
			IP=$OPTARG
			;;
		p)
			port=$OPTARG
			;;
		s)
			secure=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ $secure == '1' ] ; then
  s='s'
fi
response=$(curl --connect-timeout 10 -s -H "Host: $virtualHost" http$s://$IP:$port/alive.html)
if echo $response | grep -q alive ; then
  exit 0
else
  exit 1
fi


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
      virtualHost=$(echo $OPTARG | tr -d '[[:space:]]')
      ;;
		i)
			IP=$(echo $OPTARG | tr -d '[[:space:]]')
			;;
		p)
			port=$( echo $OPTARG | tr -d '[[:space:]]')
			;;
		s)
			secure=$( echo $OPTARG | tr -d '[[:space:]]')
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ $secure == '1' ] ; then
  s='s'
fi
response=$(curl --connect-timeout 10 -s --resolve "$virtualHost:$port:$IP" http$s://$virtualHost:$port/alive.html)
if echo $response | grep -q alive ; then
  exit 0
else
  exit 1
fi


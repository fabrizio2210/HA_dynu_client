#!/usr/bin/python2.7

# fabrizio2210 Script to keep updated DNS record on Dynu Systems

# Update your location

# Get token credential
# Enable/disable all the records. For each record in the hostname:
#   test the connectivity of the record (maybe external to this script)
#   enable if it is alive
#   disable if it is down

import requests
import json
import time
import subprocess
import argparse
import os
import sys
from base64 import b64encode

# common api-endpoint
URLbase = "https://api.dynu.com/v1/"
URLupdate = 'https://api.dynu.com/nic/update'
global accessToken
accessToken = None

#Default
timeToUpdate = 60
debug = 0
servicePort = 80
#externalTest = './isItAlive.sh'
externalTest = './isIt200.sh'

# print 
def log(msg, severity = 0):
  if severity == 1:
    print msg
  if debug == 1:
    if severity == 0:
      print msg

if os.getenv('DYNU_USER') is not None:
  user = os.getenv('DYNU_USER')
  log("Read from environment: user=" + user,1)
if os.getenv('DYNU_SECRET') is not None:
  secret = os.getenv('DYNU_SECRET')
  log("Read from environment: secret=" + secret,1)
if os.getenv('DYNU_DOMAIN_NAME') is not None:
  domain_name = os.getenv('DYNU_DOMAIN_NAME')
  log("Read from environment: domain_name=" + domain_name,1)
if os.getenv('DYNU_NODE_NAME') is not None:
  node_name = os.getenv('DYNU_NODE_NAME')
  log("Read from environment: node_name=" + node_name,1)
if os.getenv('DYNU_LOCATION') is not None:
  location = os.getenv('DYNU_LOCATION')
  log("Read from environment: location=" + location,1)
if os.getenv('DYNU_PASSWORD') is not None:
  pswToUpdate = os.getenv('DYNU_PASSWORD')
  log("Read from environment: pswToUpdate=" + pswToUpdate,1)
if os.getenv('DYNU_USERNAME') is not None:
  username = os.getenv('DYNU_USERNAME')
  log("Read from environment: username=" + username,1)
if os.getenv('DYNU_TIME_TO_UPDATE') is not None:
  timeToUpdate = os.getenv('DYNU_TIME_TO_UPDATE')
  log("Read from environment: timeToUpdate=" + timeToUpdate,1)
  timeToUpdate = int(timeToUpdate)
if os.getenv('DYNU_DEBUG') is not None:
  debug = os.getenv('DYNU_DEBUG')
  log("Read from environment: debug=" + debug,1)
  debug = int(debug)
if os.getenv('DYNU_PORT') is not None:
  servicePort = os.getenv('DYNU_PORT')
  log("Read from environment: servicePort=" + servicePort,1)
if os.getenv('DYNU_EXTERNAL_TEST') is not None:
  externalTest = os.getenv('DYNU_EXTERNAL_TEST')
  log("Read from environment: externalTest=" + externalTest,1)

parser = argparse.ArgumentParser(description='Keep update the location and check if records are available.')
parser.add_argument("-d", "--debug", help="increase output verbosity", action="store_true")
parser.add_argument("-u", "--user", help="user to access to Dynu API")
parser.add_argument("-s", "--secret", help="secret of the Dynu API, it is  used with user")
parser.add_argument("-m", "--domain-name", help="domain name to check and update")
parser.add_argument("-n", "--node-name", help="node name to check and update")
parser.add_argument("-l", "--location", help="location to check and update")
parser.add_argument("-t", "--time-to-update", type=int ,help="time in seconds between each update")
parser.add_argument("-r", "--username", help="username to access to Dynu account to update IP")
parser.add_argument("-p", "--password", help="password to update IP in Dynu account, it is used with username")
parser.add_argument("-o", "--port", help="port where the service is listen")
parser.add_argument("-x", "--external-test", help="executable to chek the availability of the service")

args = parser.parse_args()
if args.debug is not None:
  if args.debug:
    debug = 1
if args.user is not None:
  user = args.user
if args.secret is not None:
  secret = args.secret
if args.domain_name is not None:
  domain_name = args.domain_name
if args.node_name is not None:
  node_name = args.node_name
if args.location is not None:
  location = args.location
if args.time_to_update is not None:
  timeToUpdate = args.time_to_update
if args.username is not None:
  username = args.username
if args.password is not None:
  pswToUpdate = args.password
if args.port is not None:
  port = args.port
if args.external_test is not None:
  externalTest = args.external_test

if not 'user' in locals():
  log("User can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'secret' in locals():
  log("Secret can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'domain_name' in locals():
  log("Domain name can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'node_name' in locals():
  log("Node name can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'location' in locals():
  log("Location can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'pswToUpdate' in locals():
  log("Password can not be null", 1)
  parser.print_help()
  sys.exit(1)
if not 'username' in locals():
  log("Username can not be null", 1)
  parser.print_help()
  sys.exit(1)

if not os.path.isfile(externalTest):
  log("Impossible to find the test: " + externalTest, 1)
  sys.exit(1)
if not os.access(externalTest, os.X_OK):
  log("The test is not executable: " + externalTest, 1)
  sys.exit(1)

# Sanitize location
location = location.replace("-","")
location = location.replace("_","")
location = location.replace(".","")

# Ask for a new token
def getCredentials():
  log("Getting credentials")
  userAndPass = b64encode(user + ":" + secret).decode("ascii")
  HEADERS = { 'Authorization' : 'Basic %s' %  userAndPass }
  try:
    r = requests.get(url = URLbase + "oauth2/token", headers = HEADERS)
    data = r.json()
    return data['accessToken']
  except Exception as e:
    log("Error to get credentials: " + str(e), 1)
    return None

def updateIP():
  # Si aggiorna solamente se l'IP avvertito prededentemente e' diverso dall'attuale
  # Non fa testo l'interfaccia WEB
  log("Updating IP")
  PARAMS = { 'password' : pswToUpdate,
             'location' : location,
             'myip'     : '10.0.0.0',
             'username' : username}
  log(str(PARAMS))
  try:
    r = requests.get(url = URLupdate, params = PARAMS)
    log(str(r))
    return None
  except Exception as e:
    log("Error to update the IP: " + str(e), 1) 
    return None
  
def getIP():
  try:
      r = requests.get(url = 'https://api.ipify.org', params = { 'format' : 'json'})
  except:
    log("Problem during retieve my IP https://api.ipify.org", 1)
    return  None
  try:
    jsonResult = r.json()
  except:
    log("Request error: " + str(r.status_code) + " " + r.reason, 1)
    log("No return value", 1)
    return None
  return jsonResult
  
def isAvailable(virtualHost, IP, port):
  log("Verify availability for " + IP + ":" + str(port))
  rc = subprocess.call([externalTest, "-v " + virtualHost, "-i"+ IP , "-p" + str(port)])
  if rc == 0 :
    log("IP " + IP + " is UP")
    return True
  else:
    log("IP " + IP +" is DOWN")
    return False

# Try to make a request, if there is a problem of authentication get credential and try again
def makeRequest(method=None, path=None, data=None):
  if method is None:
    method = 'GET'
  global accessToken 
  if accessToken is None:
    accessToken = getCredentials()
  HEADERS = { 'Authorization' : 'Bearer ' + str(accessToken), 'Content-Type' : 'application/json' }
  try:
    if method == 'GET':
      log("Calling url: " + URLbase + path)
      r = requests.get(url = URLbase + path, headers = HEADERS)
    if method == 'POST':
      r = requests.post(url = URLbase + path, json = DATA, headers = HEADERS)
  except Exception as e:
    log("Error during the call \"" + URLbase + path +"\" : " + str(e),1)
    log("Problema con la chiamata: "+ URLbase + path , 1)
    return  None
  try:
    jsonResult = r.json()
  except:
    if r.status_code == 401:
      log("Attempting to get new token")
      accessToken = getCredentials()
      return makeRequest(method = method, path = path, data = data)
    log("Request error: " + str(r.status_code) + " " + r.reason + " during call to " + URLbase + path, 1)
    log("No return value", 1)
    return None
  return jsonResult
 

while True:

  ###########
  # UPDATE IP
  # IP are updated only for enabled records
  updateIP()
  
  ######
  # PING
  data = makeRequest(method='GET', path="ping")
  log('PING\n' + str(data))
  ##############
  # List records
  records = makeRequest(method='GET', path="dns/records/" + domain_name)
  log('RECORDS:\n' + str(records))
  
  myIP = getIP()['ip']
  log('My IP is ' + myIP)
  serviceFound = 0
  hostFound = 0
  state = u'true'
  if records is not None:
    for record in records:
      if 'ipv4_address' in record:
        if not record['ipv4_address'] is None:
          log(str(record['hostname']) + "@" + str(record['location']) + ": " + str(record['ipv4_address']))
          # Check for the records used to access to the service
          if record['node_name'] == node_name and record['domain_name'] == domain_name:
            if isAvailable(virtualHost = record['hostname'], IP = record['ipv4_address'], port = servicePort):
              # enable
              if record['state'] != True:
                log( "Enable " + str(record['hostname']) + str(record['id']), 1)
                makeRequest(path='dns/record/enable/'+str(record['id']))
            else:
              # disable
              if record['state'] != False:
                log( "Disable " + str(record['hostname']) + str(record['id']), 1)
                makeRequest(path='dns/record/disable/'+str(record['id']))

            if record['location'] == location:
              if record['ipv4_address'] == myIP:
                serviceFound = 1
                own_id = record['id']
                log( "Found own location")
              else:
                log( "Found own location, but the IP is different. Deleting it...")
                makeRequest(path='dns/record/delete/'+str(record['id']))
                # Insert as disabled so the next cycle is enabled if available
                state = u'false'

            if record['ipv4_address'] == myIP:
              if record['location'] != location:
                log("Found an duplicate IP with different location. Deleting it...")
                makeRequest(path='dns/record/delete/'+str(record['id']))

          # Check for the record that identify this host
          # Check for location.hostname.domain_name.dynu.net
          if record['node_name'] == location + '.' + node_name and record['domain_name'] == domain_name:
            if record['ipv4_address'] != myIP:
              log("Found hostname with different IP. Deleting it...")
              makeRequest(path='dns/record/delete/'+str(record['id']))
            else:
              hostFound = 1
    
  
  if serviceFound == 0:
    DATA = { u'domain_name'  : domain_name,
             u'record_type'  : u'A', 
             u'ipv4_address' : myIP,
             u'node_name'    : node_name ,
             u'location'     : location ,
             u'state'        : state }
    log('Trying to insert:\n' +  str(DATA))
    data = makeRequest(method='POST', path="dns/record/add", data=DATA)
    log(str(data))

  # Insert the location hostname
  if hostFound == 0:
    DATA = { u'domain_name'  : domain_name,
             u'record_type'  : u'A', 
             u'ipv4_address' : myIP,
             u'node_name'    : location + '.' + node_name ,
             u'location'     : location ,
             u'state'        : u'true' }
    log('Trying to insert:\n' +  str(DATA))
    data = makeRequest(method='POST', path="dns/record/add", data=DATA)
    log(str(data))

  # Update TXT record of the domain

  log("Wait for next cycle...")
  time.sleep(timeToUpdate)
 

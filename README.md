# HA_at_homes-dynu-client
It is a part of the project "HA_at_homes".

This component keeps updated the DNS records of a hostname and removes the failed nodes from the RoundRobin pool.
It is based on Dynu Systems (www.dynu.com). I choose their DNS because they let me manage the records and not only update them.

Flow
------
In an infinite loop: 
- it updates the records belong to the _location_
- it retrieves the records belog to the _node_name_ . _domain_name_
- it checks if the node pointed by the IP is alive
- it enable/disbale records if the node is alive/death

Example
-------
```
./keep_updated_record.py --user aaaabbbb-ccdd-0000-ffff-123456789012 --secret XXXXXXXXXXXXXXXXXXXXXXXXXXX \
                        --domain-name example.accesscam.org --node-name www --location myhome \
                        --password <Password in sha256>  \
                        --username <your email account> 
```
Example of entries in your Dynu Systems account:


Hostname | Type | IP Address | Location
---------| -----|------------|---------
www.example.accesscam.org | A | 10.9.0.1 | mywork
www.example.accesscam.org | A | 10.7.0.5 | myhome
www2.example.accesscam.org | A | 10.7.0.5 | myhome

When you resolve the hostname _www.example.accesscam.org_ you get a Round Robin between 10.9.0.1 and 10.7.0.5.


Parameters
----------
```
usage: keep_updated_record.py [-h] [-d] [-u USER] [-s SECRET] [-m DOMAIN_NAME]
                              [-n NODE_NAME] [-l LOCATION] [-t TIME_TO_UPDATE]
                              [-r USERNAME] [-p PASSWORD] [-o PORT]
                              [-x EXTERNAL_TEST]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           increase output verbosity
  -u USER, --user USER  user to access to Dynu API
  -s SECRET, --secret SECRET
                        secret of the Dynu API, it is used with user
  -m DOMAIN_NAME, --domain-name DOMAIN_NAME
                        domain name to check and update
  -n NODE_NAME, --node-name NODE_NAME
                        node name to check and update
  -l LOCATION, --location LOCATION
                        location to check and update
  -t TIME_TO_UPDATE, --time-to-update TIME_TO_UPDATE
                        time in seconds between each update
  -r USERNAME, --username USERNAME 
                        username to access to Dynu account to update IP               
  -p PASSWORD, --password PASSWORD 
                        password to update IP in Dynu account, it is used with 
                        username    
  -o PORT, --port PORT  port where the service is listen                                                
  -x EXTERNAL_TEST, --external-test EXTERNAL_TEST      
                        executable to chek the availability of the service  
                        
```
If your more confortable, you can pass the parameters using these environment variables:
```
DYNU_USER
DYNU_SECRET
DYNU_DOMAIN_NAME
DYNU_NODE_NAME
DYNU_LOCATION
DYNU_PASSWORD
DYNU_USERNAME
DYNU_TIME_TO_UPDATE
DYNU_DEBUG
DYNU_PORT
DYNU_EXTERNAL_TEST
```

Check of the availability
-------------------------
The availability of the node is made using an external script. If no script is specified, it will be used the _isItAlive.sh_ script.
To thescript will be passed the following parameters:
- "-v VIRTUALHOST"
- "-i IP"
- "-p PORT"

The included script will check with _curl_ if a page _http://virtualhost/alive.html_ displays the word _alive_.

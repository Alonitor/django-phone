#!/usr/bin/env python3

import re
import sys
import argparse
import requests
import vobject
import json

url = "http://127.0.0.1:8000/api/contacts/"

parser = argparse.ArgumentParser(description='export vCard FILE to REST URL')
parser.add_argument('-f','--file', nargs=1, help='vCard file')
parser.add_argument('-r','--url', nargs='?', help='REST api url', default=url)
parser.add_argument('-u','--user', nargs=1, help='REST api url user')
parser.add_argument('-p','--password', nargs=1, help='REST api url password')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
    
args = parser.parse_args()

pattern="BEGIN:VCARD.*?END:VCARD"

with open(args.file[0],'r') as f:
    result = re.findall(pattern, f.read(), re.DOTALL) 
    total = len(result)
      
    for s in result:
        v = vobject.readOne( s )

        o = {
            "name": v.fn.value,
            "vcard": s
        }

        r = requests.post(args.url, auth = (args.user[0], args.password[0]), data =o )
        print(str(total) + ": " + r.reason)
        total -= 1                
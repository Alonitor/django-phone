#!/usr/bin/env python3

import re
import sys
import argparse
import requests
import vobject
import json
import math
import time

def main():    
    url = "http://127.0.0.1:8000/api/contacts/"

    parser = argparse.ArgumentParser(description='export vCard FILE to REST URL')
    parser.add_argument('-f','--file', nargs=1, help='import vCard .vcf file')
    parser.add_argument('-r','--url', nargs='?', help='REST api url', default=url)
    parser.add_argument('-u','--user', nargs=1, help='REST api url user')
    parser.add_argument('-p','--password', nargs=1, help='REST api url password')
    parser.add_argument('-e','--export', action='store_true', help='export SYNC items to vCard .vcf file')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    print(args)

    if not (args.file is None):
        import_cvf(args.file[0], args.url, args.user[0], args.password[0] )
        
    if args.export:
        export_cvf(args.url, args.user[0], args.password[0] )

        
def import_cvf(file, url, user, password):
    print("importing file: " + file)
    pattern="BEGIN:VCARD.*?END:VCARD"

    with open(file,'r') as f:
        result = re.findall(pattern, f.read(), re.DOTALL) 
        total = len(result)

        for s in result:
            v = vobject.readOne( s )

            o = {
                "name": v.fn.value,
                "vcard": s
            }

            r = requests.post(url, auth = (user, password), data =o )
            print(str(total) + ": " + r.reason)
            total -= 1                
        

def export_cvf(url, user, password, sync=2):   
#sync=2 equals sync=True
    page = 1    
    contact_list = []
    while True:
        url += "?sync=" + str(sync) + "&page=" + str(page)
        r = requests.get(url, auth = (user, password))
        j = json.loads(r.content)    
        contact_list += [ c['vcard'] for c in j['results'] ]
        
        total = j['count']
        page += 1
        print(str( len(contact_list) ) + " / " + str(total) )
        
        if len(contact_list) == total: 
            print("Last 3 items:")
            print(contact_list[-3:])           
        
            path = 'export_contacts_' + str(time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))) + '.vcf'
            f=open(path,'w',encoding='utf-8')
            content=f.write('\n\n'.join(contact_list)  )
            f.close()

            return

if __name__ == "__main__": main()
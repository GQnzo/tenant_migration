# Simple example to read creds file, connect to API, and print detections.

##################################################################################
# USAGE
#
##################################################################################
from __future__ import print_function
import json
from pprint import pprint
import cyapi.cyapi as cy
from cyapi.cyapi import CyAPI
import argparse

__VERSION__ = '1.0'

##################################################################################
# Arguments
#
##################################################################################
def ParseArgs():

    regions = []
    regions_help =  "Region the tenant is located: "
    for (k, v) in CyAPI.regions.items():
        regions.append(k)
        regions_help += " {} - {} ".format(k,v['fullname'])

    parser = argparse.ArgumentParser(description='Create a new OPTICS Rule Set based on an existing on and best practice phases.', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    # Cylance SE Tenant
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')
    parser.add_argument('-c2', '--creds2_file', dest='creds2', help='Path to JSON File with API info provided')


    return parser

##################################################################################
# Tenant Integration
# Modify the keys to align with your tenant API
##################################################################################
# Cylance SE Tenant
##################################################################################

commandline = ParseArgs()
args = commandline.parse_args()

if args.debug_level:
    cy.debug_level = args.debug_level

if args.creds2:
    with open(args.creds2, 'rb') as f:
        creds2 = json.loads(f.read())

    if not creds2.get('region'):
        creds2['region'] = args.region

    API2 = CyAPI(**creds2)

if args.creds:
    with open(args.creds, 'rb') as f:
        creds = json.loads(f.read())

    if not creds.get('region'):
        creds['region'] = args.region

    API = CyAPI(**creds)

elif args.tid_val and args.app_id and args.app_secret:
    tid_val = args.tid_val
    app_id = args.app_id
    app_secret = args.app_secret
    API = CyAPI(tid_val,app_id,app_secret,args.region)

else:
    print("[-] Must provide valid token information")
    exit(-1)

API.create_conn()
get_rules = API.get_detection_rules()
rule_ids = [x['Id'] for x in get_rules.data if x['Category'] == "Custom"]
get_rule_det = API.get_bulk_detection_rule(rule_ids)
rule_det = [x for x in get_rule_det.data]


API2.create_conn()
for rule in rule_det:
    # rule = {k.lower(): v for k, v in rule.items()}
    rule = json.dumps(rule, sort_keys=True)
    x = API2.create_detection_rule(rule)
    print("TTT")

print("")
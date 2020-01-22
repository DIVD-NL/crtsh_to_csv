#!/usr/bin/env python

import argparse
import requests
import re
import json

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('domains', metavar='D', type=str, nargs='+',
                    help='Domain to query')
parser.add_argument('--wildcard', '-w', action='store_true', help='Query wildcard for domain')
args = parser.parse_args()

for domain in args.domains:
    session = requests.Session()
    if args.wildcard:
        domain = "*.{}".format(domain)
    query_json = session.get("https://crt.sh/?q={}&output=json".format(domain))
    certs = json.loads(query_json.text)
    for cert in certs:
        if cert["name_value"] == domain:
            print('"{}";"{}";{};{};"{}"'.format(domain,cert["id"],cert["not_before"],cert["not_after"],cert["issuer_name"]))

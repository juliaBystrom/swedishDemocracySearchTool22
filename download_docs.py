#! /usr/bin/python3

import requests
import os
import json

search_url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=datum&sortorder=desc&rapport=&utformat=json&a=s#soktraff'
doc_data = json.loads(requests.get(url=search_url).text)
docs = {}

i = 0
while('@nasta_sida') in doc_data['dokumentlista']:
 print('Downloading page {}'.format(i))
 i += 1
 doc_data = json.loads(requests.get(url=doc_data['dokumentlista']['@nasta_sida']).text)
 for doc in doc_data['dokumentlista']['dokument']:
  docs[doc['dok_id']] = doc

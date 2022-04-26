import pandas as pd
from bs4 import BeautifulSoup

import requests
import os
import json




def get_text(id):
    url = "https://data.riksdagen.se/dokumentstatus/" + str(id) 
    response = requests.get(url)
    soup1 = BeautifulSoup(response.text, 'lxml')
    dokument = soup1.dokumentstatus.dokument
    
    soup2 = BeautifulSoup(dokument.get_text(), 'html.parser')
    text = soup2.get_text()
    
    return text


def get_docs_dictionary():
    search_url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=datum&sortorder=desc&rapport=&utformat=json&a=s#soktraff'
    doc_data = json.loads(requests.get(url=search_url).text)
    docs = {}

    i = 0
    while('@nasta_sida') in doc_data['dokumentlista']:
        print('Downloading page {}'.format(i))
        i += 1
        doc_data = json.loads(requests.get(url=doc_data['dokumentlista']['@nasta_sida']).text)
        break

    for doc in doc_data['dokumentlista']['dokument']:
        #print(doc['dok_id'])
        docs[doc['dok_id']] = doc

    return docs

def create_document(text, doc_info):
    publicerad: str = doc_info['publicerad']
    pdf_url: str = doc_info['filbilaga']['fil']['url']
    summary: str = doc_info['summary']
    rm: str= doc_info['rm']
    beteckning: str = doc_info['beteckning']
    doktyp: str = doc_info['doktyp']

    document = {
        'text': text,
        'publicerad': publicerad,
        'pdf_url': pdf_url,
        'summary': summary,
        'rm': rm,
        'beteckning': beteckning,
        'doktyp':doktyp,
    }

    return document
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import json
import re
import sys


def get_references(text, doc_name):
    ref = re.findall('\(SOU \d{4}:\d+\w*\d*\)', text)
    reference_list = []
    for r in ref:
        try:
            rm = r[5:9]
            nummer = r[10:-1]
            reference = str(rm) + ":" + str(nummer)
            if reference not in reference_list and reference != doc_name:
                reference_list.append(reference)
        except Exception:
            pass
    return reference_list

def get_doc_text(id):
    print('Getting text from id: {}'.format(id))
    url = "https://data.riksdagen.se/dokumentstatus/" + str(id)
    response = requests.get(url)
    soup1 = BeautifulSoup(response.text, 'lxml')
    try:
        dokument = soup1.dokumentstatus.dokument
    except AttributeError:
        print(f"Dokument field missing in document {id}, skipping.", file=sys.stderr)
        return ""

    try:
        soup2 = BeautifulSoup(dokument.get_text(), 'html.parser')
    except AssertionError:
        print(f"Invalid HTML in document {id}, skipping.", file=sys.stderr)
        return ""

    text = soup2.get_text()
    text = re.sub(r'- och', ' och', text)
    #test = re.sub(r'-/', ' ', test) don't need
    text = re.sub(r'- ', '', text)
    return text

def get_docs_dictionary():
    search_url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=datum&sortorder=asc&rapport=&utformat=json&a=s#soktraff'
    #TEST: search_url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=2000&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=datum&sortorder=asc&rapport=&utformat=json&a=s#soktraff'
    #TEST: search_url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=1990-01-01&tom=1995-12-31&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=rel&sortorder=asc&rapport=&utformat=json&a=s#soktraff'
    doc_data = json.loads(requests.get(url=search_url).text)
    docs = {}
    for doc in doc_data['dokumentlista']['dokument']:
        #print(doc['dok_id'])
        docs[doc['dok_id'].lower()] = doc

    i = 0
    while('@nasta_sida') in doc_data['dokumentlista']:
        print('Downloading page {}'.format(i))
        i += 1
        doc_data = json.loads(requests.get(url=doc_data['dokumentlista']['@nasta_sida']).text)
        for doc in doc_data['dokumentlista']['dokument']:
            #print(doc['dok_id'])
            docs[doc['dok_id'].lower()] = doc

    return docs

def create_document(text, doc_info, ref_out=None):
    publicerad: str = doc_info['publicerad']
    pdf_url: str = ""
    if doc_info['filbilaga'] is not None:
        pdf_url: str = doc_info['filbilaga']['fil']['url']
    summary: str = doc_info['summary']
    rm: str = doc_info['rm']
    nummer: str = doc_info['nummer']
    doktyp: str = doc_info['doktyp']
    ref_out: str = ref_out
    ref_in: list = []
    document = {
        'text': text,
        'publicerad': publicerad,
        'pdf_url': pdf_url,
        'summary': summary,
        'rm': rm,
        'nummer': nummer,
        'doktyp':doktyp,
        'ref_out': ref_out,
        'ref_in': ref_in
    }

    return document

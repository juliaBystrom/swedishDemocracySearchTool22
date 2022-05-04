from pydoc import doc
import sys
sys.path.append('/Users/Celine/opt/anaconda3/lib/python3.9/site-packages')
import numpy as np
from ElasticInstance import *
from sknetwork.ranking import PageRank
import pandas as pd
import requests


def update_document_pagerank(el_inst, pr_scores, index_name):
    for _, (id, score) in enumerate(pr_scores.items()):
        el_inst.update_document(index_name, {'pagerank': score}, id)
    
def create_transition_matrix(ids, el_inst, index_name):
    df = pd.DataFrame(data=0.0, index=ids, columns=ids)
    not_found = []
    p = 0
    for i in range(len(df)):
        print("Doc", i, "out of", len(df))
        doc_id = df.iloc[i].name
        doc = el_inst.get_document_by_id(index_name, doc_id)
        if doc is not None:
            from_doc = doc['_id']
            ref_out = doc['_source']['ref_out']
            if ref_out != []:
                for to_doc in ref_out:
                    if to_doc in df.columns:
                        df[to_doc][from_doc] = np.round(1/len(ref_out), 3)
        else:
            not_found.append(doc_id)

        # Save progress to file
        if i == 100:
            df = df.iloc[p:i]
            df.to_csv('transition_matrix.csv', header=False)
            df = pd.DataFrame(data=0.0, index=ids, columns=ids)
            p =i
        elif i%100==0 and i !=0:
            df = df.iloc[p:i]
            df.to_csv('transition_matrix.csv', header=False, mode='a')
            df = pd.DataFrame(data=0.0, index=ids, columns=ids)
            p = i
        if i == len(df)-1:
            df = df.iloc[p:]
            df.to_csv('transition_matrix.csv', header=False, mode='a')
    return not_found

def get_pageranks(el_inst, index_name):
    # Get all ids 
    url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=rel&sortorder=asc&rapport=&utformat=iddump&a=s#soktraff'
    response = requests.get(url)
    ids = response.text.split(',')
            
    # Create transition matrix (TM)
    not_found = create_transition_matrix(ids, el_inst, index_name)
    print("Could not find", len(not_found), "documents.\n")
    for n_id in not_found:
        print(n_id)
    
    # Load TM from file
    df = pd.read_csv('transition_matrix.csv', names=ids, header=None)

    # Compute PageRank
    pr = PageRank()
    scores = pr.fit_transform(df.to_numpy())
    pr_scores = dict(zip(ids, scores))

    # Update PageRank in index 
    update_document_pagerank(el_inst, pr_scores, index_name)

el_inst = ElasticInstance()
index_docs = 'demo3'
#fetch_and_add_data_to_es(el_inst)
get_pageranks(el_inst, index_docs)

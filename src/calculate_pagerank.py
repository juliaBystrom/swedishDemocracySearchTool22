import sys
sys.path.append('/Users/Celine/opt/anaconda3/lib/python3.9/site-packages')
import numpy as np
from ElasticInstance import *
from sknetwork.ranking import PageRank
import pandas as pd
import requests
   
def update_document_pagerank(el_inst, pr_scores):
    pass
    #for _, (id, score) in enumerate(pr_scores):
        #doc = el_inst.get_document_by_id(id)
        #{'pagerank': score}
    
def create_transition_matrix(ids, el_inst, index_name):
    df = pd.DataFrame(data=0.0, index=ids, columns=ids)
    for i in range(len(df)):
        from_doc = df.iloc[i].name
        if from_doc is not None:
            to_doc = el_inst.get_document_by_id(index_name, from_doc)
            if to_doc is not None:
                ref_out = to_doc['_source']['ref_out']
                #ref_out = ['gvb386', 'hab317', 'hab312', 'hab318'] # only for testing
                if ref_out is not None:
                    for to_doc in ref_out:
                        df[to_doc][from_doc] = 1/len(ref_out)
    return df
#el_inst = ElasticInstance()

def get_pageranks(el_inst, index_name):
    # Get all ids 
    url = 'https://data.riksdagen.se/dokumentlista/?sok=&doktyp=sou&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=&avd=&webbtv=&talare=&exakt=&planering=&facets=&sort=rel&sortorder=asc&rapport=&utformat=iddump&a=s#soktraff'
    response = requests.get(url)
    ids = response.text.split(',')
    
    # Create transition matrix
    df = create_transition_matrix(ids, el_inst, index_name)

    # Compute PageRank
    pr = PageRank()
    scores = pr.fit_transform(df.to_numpy())
    pr_scores = dict(zip(ids, scores))

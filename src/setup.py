from ElasticInstance import *
from get_doc_info import create_document, get_text, get_docs_dictionary


def fetch_and_add_data_to_es(el_inst: ElasticInstance):
    docs = get_docs_dictionary()

    ids = []
    for id, v in docs.items():
        ids.append(id)
        text = get_text(id)
        document = create_document(text, v)
        el_inst.add_to_index("emil", document, id )


def search_data(el_inst: ElasticInstance):

    res = el_inst.search_index("emil", "text", "terrorism")
    print("Found ", len(res) ," documents.")
    for r in res:
        print("{} {}:{}".format(r['_source']['doktyp'], r['_source']['rm'], r['_source']['beteckning']))


el_inst = ElasticInstance()
el_inst.create_index("emil")
fetch_and_add_data_to_es(el_inst)
search_data(el_inst)

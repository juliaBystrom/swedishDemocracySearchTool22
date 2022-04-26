from ElasticInstance import *
from get_doc_info import create_document, get_doc_text, get_docs_dictionary, get_references



def fetch_and_add_data_to_es(el_inst: ElasticInstance):
    docs = get_docs_dictionary()

    ids = []
    for id, v in docs.items():
        ids.append(id)
        text = get_doc_text(id)
        references = get_references(text)
        document = create_document(text, v)
        el_inst.add_to_index("demo", document, id )  



def search_data(el_inst: ElasticInstance):
    
    res = el_inst.search_index("demo", "text", "ningsområden")
    print("Found ", len(res) ," documents.")
    # print(res[0])

el_inst = ElasticInstance()
search_data(el_inst)
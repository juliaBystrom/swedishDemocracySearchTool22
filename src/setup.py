from ElasticInstance import *
from download_docs import get_docs_dictionary

el_inst = ElasticInstance()
docs = get_docs_dictionary()

ids = []
for k, v in docs.items():
    ids.append(k)
    el_inst.add_to_index("riksdagen", v, k ) 


print(el_inst.get_document_by_id("riksdagen", "H9B3103"))
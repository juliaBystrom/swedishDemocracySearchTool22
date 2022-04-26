from ElasticInstance import *
from get_doc_info import create_document, get_doc_text, get_docs_dictionary, get_references

index_docs = "demo2"
index_names = "names_to_id"

def fetch_and_add_data_to_es(el_inst: ElasticInstance):
    docs = get_docs_dictionary()

    ids = []
    for id, v in docs.items():
        ids.append(id)
        text = get_doc_text(id)
        ref_out_names = get_references(text)
        ref_out_ids = []
        doc_name = str(v["rm"]) + ":" + str(v["nummer"])
        el_inst.add_name(index_names, doc_name, id) 
        
        #print("id", id)
        #print("refs", ref_out_names)
        
        for doc_name in ref_out_names:
            ref_out_id = el_inst.get_id_by_name(index_names, doc_name)
            if ref_out_id is not None:
                ref_out_ids.append(ref_out_id) 
                ref_doc = el_inst.get_document_by_id(index_docs, ref_out_id)
                ref_doc["_source"]["ref_in"].append(id)
                #el_inst.update_document(index_docs, ref_doc, id)        # Updates the referred docs with id of current doc. 

        document = create_document(text, v, ref_out_ids)
        el_inst.add_to_index(index_docs, document, id )
        

def search_data(el_inst: ElasticInstance):
    
    res = el_inst.search_index("demo", "text", "ningsområden")
    print("Found ", len(res) ," documents.")

el_inst = ElasticInstance()
fetch_and_add_data_to_es(el_inst)
#search_data(el_inst)
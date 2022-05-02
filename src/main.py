from typing import Optional
from fastapi import FastAPI, Query


from ElasticInstance import ElasticInstance
from elastic_helpers import get_date_query, get_search_string_match_query


elastic = ElasticInstance()
app = FastAPI()
INDEX_NAME = "demo2"

"""
Default rote
"""
@app.get("/")
async def read_root():
    return {"SwedishDemocracySearchTool22": "Welcome to Swedish Democracy Search Tool 22"}

"""
Returns document by id

"""
@app.get("/document/{id}")
async def read_item(id: str, text: bool = False):
    doc = elastic.get_document_by_id(INDEX_NAME, id)
    if not doc:
        return {"error": "Document not found"}
    if text:
        return doc
    else:
        doc['_source'].pop('text')
        return doc

"""
Returns all documents matching the search query. 
        Parameters:
            search_string: String to be searched
            start_date: Start date for filtering the search (YYYY-MM-DD)
            end_date: End date for filtering the search (YYYY-MM-DD)
            text: If true, the text field will be returned
            phrase_search: If True, the search will be performed with a phrase search


"""
@app.get("/documents/search/")
async def read_item(search_string: str = None, start_date: str =None, end_date: str=None, text: bool = False, phrase_search: bool = False):
    print("search_string: ", search_string, "start_date: ", start_date, "end_date: ", end_date, "text: ", text, "phrase_search: ", phrase_search)

    # Create the query used by elastic search
    
    date_filter = {}
    search_string_filter = {}

    # If the user has specified a start date or a end date, create the date filter
    if start_date or end_date:
        date_filter = get_date_query(start_date=start_date, end_date=end_date)
    # If the user have specified a search string, create the search string filter
    if search_string:
        search_string_filter = get_search_string_match_query("text", search_string, phrase_search)
    
    # Combine the filters into a single query
    query = { "query": {"bool": {  **search_string_filter,  **date_filter}}}
    # Search the index
    docs = elastic.search_index_custom_query(INDEX_NAME, query)
    print("Found ", len(docs) ," documents.")

    # If no docs was found return an empty list
    if not docs:
        return []


    # Sort docs


    # If the user has specified that the text field should be returned, return the text field for each document.
    if text:
        return docs
    else:
        # Remove the text field from the documents
        for doc in docs:
            doc['_source'].pop('text')
        return docs


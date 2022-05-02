from elasticsearch import Elasticsearch, helpers, NotFoundError
import configparser


class ElasticInstance:

    default_mapping = {
        "properties": {
            "text":       { "type": "text" },
            "publicerad": { "type": "date" },
            "pdf_url":    { "type": "keyword" },
            "summary":    { "type": "text" },
            "rm":         { "type": "integer" },
            "beteckning": { "type": "integer" },
            "doktyp":     { "type": "keyword" },
            "referenser": { "type": "keyword" }
        }
    }

    default_settings = {
        "analysis": {
            "analyzer": {
                "default": {
                    "tokenizer": "standard",
                    "filter": [ "lowercase", "snöboll" ]
                }
            },
            "filter": {
                "snöboll": {
                    "type": "snowball",
                    "language": "Swedish"
                }
            }
        }
    }

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('example.ini')

        self.es = Elasticsearch(
            hosts=[config['DEFAULT']['host']],
            basic_auth=(config['DEFAULT']['basic_user'], config['DEFAULT']['basic_pass']),
        )

    def test_connection(self):
        output = self.es.info()
        print(output)

    def refresh_index(self, index_name):
        self.es.indices.refresh(index=index_name)

    """
        Creates an index with the appropriate mappings.

            Args:
                index_name (str): The name of the index.
    """
    def create_index(self, index_name):
        # TODO: Better error handling
        if self.es.indices.exists(index=index_name):
            return None

        return self.es.indices.create(
            index=index_name,
            mappings=self.default_mapping,
            settings=self.default_settings
        )

    """
        Deletes an index.
    """
    def delete_index(self, index_name):
        self.es.indices.delete(index=index_name)

    """
        Creates or updates a document in an index.

            If an index with the given name does not exist, returns None.
            If a document with the given id already exists, it is updated.

            Args:
                index_name (str): The name of the index.
                document_id optional(str): The id of the document. If not given, a new id is generated.
    """
    def add_to_index(self, index_name, document, document_id=None):

        try:
            if document_id is None:
                # No explicit id given to the inserted document.
                return self.es.index(
                    index=index_name,
                    document=document,
                )
            else:
                return self.es.index(
                    index=index_name,
                    id=document_id,
                    document=document
                )
        except Exception:
            return None

    def add_name(self, index_name, doc_name, doc_id):
        return self.es.index(
                    index=index_name,
                    id=doc_name,
                    document={"doc_id":doc_id}
                )


    """
        Args:
            index_name: Name of the index containing the document to be updated
            id: Id of the document to be updated
            document: An object containing the fields and their new values.
                      If the fields does not exist, they will be added to the document.

    """
    def update_document(self, index_name, document, document_id):
        try:
            return self.es.update(
                index=index_name,
                id=document_id,
                doc=document
                )
        except NotFoundError:
            print(f"[Error] Can not update document with id {document_id} because it was not found")
            return None

    """
        Args:
            index_name: Name of the index to be searched
            field: Field to be used for the search
            search_string: String to be searched
    """
    def search_index(self, index_name, field, search_string):
        result = self.es.search(
            index=index_name,
            body={ 'query': {
                'match': {field: search_string}
            }}
        )
        return result['hits']['hits']

    """
        Args:
            index_name: Name of the index to be searched
            query: query to be used for the search
    """
    def search_index_custom_query(self, index_name, query):
        result =  self.es.search(
            index=index_name,
            body= query
        )
        return result['hits']['hits']

    def get_document_by_id(self, index_name, document_id):
        try:
            return self.es.get(index=index_name, id=document_id)
        except NotFoundError:
            print(f"[Error] Document with id {document_id} was not found")
            return None

    def get_id_by_name(self, index_name, doc_name):
        try:
            #print(self.es.get(index=index_name, id=doc_name))
            return self.es.get(index=index_name, id=doc_name)["_source"]["doc_id"]
        except NotFoundError:
            print(f"[Error] Document with name {doc_name} was not found")
            return None

    def delete_document_by_id(self, index_name, document_id):
        try:
            return self.es.delete(index=index_name, id=document_id)
        except NotFoundError:
            print(f"[Error] Can not delete document with id {document_id} because it was not found")
            return None

    def document_exists(self, index_name, document_id):
        try:
            self.es.exists(index=index_name, id=document_id)
            return True
        except NotFoundError:
            return False

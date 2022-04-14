from elasticsearch import Elasticsearch, helpers, NotFoundError
import configparser



class ElasticInstance:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('example.ini')

        self.es = Elasticsearch(
            cloud_id=config['DEFAULT']['cloud_id'],
            api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
        )

    def test_connection(self):
        output = self.es.info()
        print(output)

    def refesh_index(self, index_name):
        self.es.indices.refresh(index=index_name)

    """
        Creates or updates a document in an index. 
        
            If an index with the given name does not exist, it is created.
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
                    document=document
                )
            else:
                return self.es.index(
                    index=index_name,
                    id=document_id,
                    document=document
                )
        except Exception:
            return None


    """
        Args:
            index_name: Name of the index containing the document to be updated
            id: Id of the document to be updated
            document: An object containing the fields and their new values.
                      If the fields does not exist, they will be added to the document.
    
    """
    def update_document(self, index_name, document_id, document):

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
        result =  self.es.search(
            index=index_name,
            query={
                'match': {field: search_string}
            }
        )
        return result['hits']['hits']

    def get_document_by_id(self, index_name, document_id):
        try:  
            return self.es.get(index=index_name, id=document_id)
        except NotFoundError:
            print(f"[Error] Document with id {document_id} was not found")
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
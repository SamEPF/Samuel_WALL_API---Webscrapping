import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreClient:
    """Wrapper around a Firestore database"""

    def __init__(self) -> None:
        """Init the client."""
        cred = credentials.Certificate("/Users/samwall/Documents/5A/Samuel_WALL_API---Webscrapping/TP2 and  3/services/epf-flower-data-science/firebase_credentials.json")
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def get(self, collection_name: str, document_id: str) -> dict:
        """Find one document by ID.
        Args:
            collection_name: The collection name
            document_id: The document id
        Return:
            Document value.
        """
        doc = self.client.collection(collection_name).document(document_id).get()
        if doc.exists:
            return doc.to_dict()
        raise FileNotFoundError(
            f"No document found at {collection_name} with the id {document_id}"
        )

    def set(self, collection_name: str, document_id: str, data: dict) -> None:
        """Set a document in the collection.
        Args:
            collection_name: The collection name
            document_id: The document id
            data: The data to set in the document
        """
        self.client.collection(collection_name).document(document_id).set(data)
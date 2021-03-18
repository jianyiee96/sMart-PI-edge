import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cert_path = "files/smart-mobile-application-de8a1d29af3c.json"
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_firebase_collection_ref(collection: str):
    """
    Returns the Firebase reference of specified collection.
    """
    return db.collection(collection)

def get_firebase_document_ref(collection: str, document_id: str):
    """
    Returns the Firebase reference of specified collection and document id.
    """
    return db.collection(collection).document(document_id)     

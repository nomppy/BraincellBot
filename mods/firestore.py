import firebase_admin
from firebase_admin import firestore


app = firebase_admin.initialize_app()
db = firestore.client(app)


def _write(path, data, merge=True):
    doc_ref = db.document(path)
    doc_ref.set(data, merge=merge)


def _update(path, data):
    doc_ref = db.document(path)
    doc_ref.update(data)

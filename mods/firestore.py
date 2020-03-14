import firebase_admin
from firebase_admin import firestore


app = firebase_admin.initialize_app()
db = firestore.client(app)


def _write(path, data, merge=True):
    ref = db.document(path)
    ref.set(data, merge=merge)


def _update(path, data):
    ref = db.document(path)
    ref.update(data)


def _delete(path):
    db.document(path).delete()


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)
import firebase_admin
from firebase_admin import firestore


def update_field(ref, field, value):
    ref.update({field: value})


class Firestore:
    def __init__(self):
        app = firebase_admin.initialize_app()
        self.db = firestore.client(app)

    def _write(self, path, data, merge=True):
        ref = self.db.document(path)
        ref.set(data, merge=merge)

    def _update(self, path, data):
        ref = self.db.document(path)
        ref.update(data)

    def _delete(self, path):
        self.db.document(path).delete()

    def delete_collection(self, coll_ref, batch_size):
        docs = coll_ref.limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            doc.reference.delete()
            deleted += 1

        if deleted >= batch_size:
            return self.delete_collection(coll_ref, batch_size)
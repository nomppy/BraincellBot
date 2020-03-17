import os
import json

import firebase_admin
from firebase_admin import firestore


# avoid initializing multiple instances of the same app
try:
    app = firebase_admin.get_app('firestore')
except ValueError:
    cred = firebase_admin.credentials.Certificate(json.loads(os.getenv('GOOGLE_CRED')))
    app = firebase_admin.initialize_app(cred, name='firestore')

db = firestore.client(app)


def update_field(ref, field, value):
    ref.update({field: value})


def _get_doc(path):
    ref = db.document(path)
    return ref.get().to_dict()


def get_user(uid):
    return _get_doc(f'users/{uid}')


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


def update_user(uid, self_, new_token=None, new_email=None, new_pwd=None):
    path = f'users/{uid}'
    data = {
        'token': new_token,
        'email': new_email,
        'pwd': new_pwd,
        'self': self_
    }
    _update(path, data)


def add_user(uid, self_, token=None, email=None, pwd=None):
    path = f'users/{uid}'
    data = {
        'token': token,
        'email': email,
        'pwd': pwd,
        'self': self_
    }
    _write(path, data)


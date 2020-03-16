import os
import json

import firebase_admin
from firebase_admin import firestore


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


def _get_user(uid):
    return _get_doc(f'users/{uid}')


def get_user_token(uid):
    return _get_user(uid)['token']


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


def add_user(uid, self_hosting, token=None, email=None, pwd=None):
    path = f'users/{uid}'
    data = {
        'token': token,
        'email': email,
        'pwd': pwd,
        'self': self_hosting
    }
    _write(path, data)

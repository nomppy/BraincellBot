import os
import json

import firebase_admin
from firebase_admin import firestore
from Naked.toolshed.shell import execute_js, muterun_js


# avoid initializing multiple instances of the same app
try:
    app = firebase_admin.get_app('firestore')
except ValueError:
    cred = firebase_admin.credentials.Certificate(json.loads(os.getenv('GOOGLE_CRED')))
    app = firebase_admin.initialize_app(cred, name='firestore')

db = firestore.client(app)


async def update_field(uid: str, field, value):
    await _write(f'users/{uid}', {field: value})


async def update_command(uid: str, command: str, field, value):
    await _write(f'users/{uid}/commands/{command}', {field: value})


async def update_command_fields(uid: str, command: str, field_values: dict):
    await _write(f'users/{uid}/commands/{command}', field_values)


async def _get_doc(path):
    ref = db.document(path)
    return ref.get().to_dict()


async def get_user(uid: str):
    return await _get_doc(f'users/{uid}')


async def delete_user(uid):
    await delete_collection(f'users/{uid}/commands')
    await _delete(f'users/{uid}')


async def _write(path, data, merge=True):
    ref = db.document(path)
    ref.set(data, merge=merge)


async def _update(path, data):
    ref = db.document(path)
    ref.update(data)


async def _delete(path):
    db.document(path).delete()


async def get_command(uid: str, command: str):
    return await _get_doc(f'users/{uid}/commands/{command}')


async def delete_collection(path):
    success = execute_js('mods/delete_collection.js', path)
    if success:
        return 'Deleted collection'
    else:
        return 'Failed to delete collection'


async def update_user(uid, self_, username=None, new_token=None, new_email=None, new_pwd=None, prefix=None, active=True):
    path = f'users/{uid}'
    data = {
        'username': username,
        'token': new_token,
        'email': new_email,
        'pwd': new_pwd,
        'self': self_,
        'prefix': prefix,
        'active': active
    }
    await _update(path, data)


async def add_user(uid, self_, username=None, token=None, email=None, pwd=None, prefix='b!', active=True):
    path = f'users/{uid}'
    data = {
        'username': username,
        'token': token,
        'email': email,
        'pwd': pwd,
        'self': self_,
        'prefix': prefix,
        'active': active
    }
    await _write(path, data)


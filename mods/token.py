import json
import os

import firebase_admin
from firebase_admin import auth
from mods import firestore


try:
    app = firebase_admin.get_app('auth')
except ValueError:
    cred = firebase_admin.credentials.Certificate(json.loads(os.getenv('GOOGLE_CRED')))
    app = firebase_admin.initialize_app(cred, name='auth')


def create_custom_token(uid: str):
    custom_token = auth.create_custom_token(uid, app=app)
    return custom_token


def refresh_custom_token(uid):
    auth.revoke_refresh_tokens(uid, app=app)
    return create_custom_token(uid)


def revoke_refresh_tokens(uid):
    auth.revoke_refresh_tokens(uid, app=app)


def token_exists(uid: str):
    token = firestore.get_user_token(uid)
    return token is not None



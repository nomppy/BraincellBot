import firebase_admin
from firebase_admin import auth


app = firebase_admin.initialize_app()


def create_custom_token(uid):
    custom_token = auth.create_custom_token(uid)
    return custom_token


def refresh_custom_token(uid):
    auth.revoke_refresh_tokens(uid)
    return create_custom_token(uid)

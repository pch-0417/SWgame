import firebase_admin
from firebase_admin import credentials, storage
import io

cred = credentials.Certificate("swgame.json")
if not firebase_admin._apps: 
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'SWgame.appspot.com'
    })
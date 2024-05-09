import firebase_admin
from firebase_admin import credentials
import pyrebase
from configs.firebase_config import firebaseConfig
from dotenv import dotenv_values

nfig = dotenv_values(".env")

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "configs/todolist-9ea3d-firebase-adminsdk-g3yqt-73d47c2b5a.json"
    )
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

authShop = firebase.auth()

# cred = credentials.Certificate(json.load(config))

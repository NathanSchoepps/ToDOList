import firebase_admin, pyrebase
from firebase_admin import credentials
import json
import os
from dotenv import load_dotenv

load_dotenv()
env={
  "FIREBASE_SERVICE_ACCOUNT_KEY": os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"),
  "FIREBASE_CONFIG": os.getenv("FIREBASE_CONFIG")
}

cred = credentials.Certificate(json.loads(env['FIREBASE_SERVICE_ACCOUNT_KEY'], strict=False))
firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(json.loads(env['FIREBASE_CONFIG'], strict=False))
db=firebase.database()
authShop = firebase.auth()
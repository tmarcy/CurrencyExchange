from flask import Flask
from flask_wtf import CSRFProtect
import app_config
import appengine_config


app = Flask(__name__)
app.config.from_object(__name__)

if appengine_config.GAE_DEV:
    app.secret_key='my-secret-key'
    app.debug=True
else:
    app.secret_key=app_config.app_secure_key

DEBUG = True
csrf_protect = CSRFProtect(app)

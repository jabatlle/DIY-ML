import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
from .celery import make_celery

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017/doc_analyzer'
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)
db = mongo.db

UPLOAD_FOLDER = '/Users/josealejandrobatlle/Documents/530/DIY-ML/uploads'  # Update this path
ALLOWED_EXTENSIONS = {'pdf'}

uploads = UploadSet('documents', DOCUMENTS)
app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_FOLDER  # Set the upload destination
configure_uploads(app, uploads)

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND

celery = make_celery(app)

from app import routes

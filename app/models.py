from datetime import datetime
from app import db

class User:
    def __init__(self, id, name, email, date=None):
        self.id = id
        self.name = name
        self.email = email
        self.date = date or datetime.utcnow()

class Document:
    def __init__(self, title, id, summary=None):
        self.title = title
        self.id = id
        self.summary = summary

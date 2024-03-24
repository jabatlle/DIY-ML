# Smart Document Analyzer

Smart Document Analyzer is a Flask-based REST API application for secure file uploading, text NLP analysis, and MongoDB integration. It allows users to upload documents, perform text analysis, and manage user data securely.

## Features

- Secure file uploader/ingester
- Text NLP analysis
- CRUD operations for users and documents
- MongoDB integration for data storage

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- MongoDB

## Installation

1. Clone the repository:

git clone [<repository-url>](https://github.com/jabatlle/DIY-ML/tree/main)
cd DIY-ML


2. Install dependencies:

pip install -r requirements.txt


## Configuration

Set up your MongoDB URI in `config.py`:

```python
MONGO_URI = 'mongodb://localhost:27017/doc_analyzer'

Usage
Run the application:

python3 run.py

The application will be available at http://localhost:5000.

API Endpoints
GET /users: Retrieve all users
POST /users: Create a new user
GET /users/<id>: Retrieve a specific user by ID
PUT /users/<id>: Update a specific user by ID
DELETE /users/<id>: Delete a specific user by ID
GET /documents: Retrieve all documents
POST /documents: Create a new document
GET /documents/<id>: Retrieve a specific document by ID
PUT /documents/<id>: Update a specific document by ID
DELETE /documents/<id>: Delete a specific document by ID
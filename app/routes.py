import os
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from .utils import allowed_file
from app import app, db, uploads, celery

blueprint = Blueprint('api', __name__)

# User Endpoints
@blueprint.route('/users', methods=['GET'])
def get_users():
    users_collection = db['users']
    users = list(users_collection.find())
    return jsonify(users), 200

@blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    users_collection = db['users']
    user_data = {
        'name': data['name'],
        'email': data['email'],
        'date': datetime.utcnow()
    }
    result = users_collection.insert_one(user_data)
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)}), 201

@blueprint.route('/users/<id>', methods=['GET'])
def get_user(id):
    users_collection = db['users']
    user = users_collection.find_one({'_id': ObjectId(id)})
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@blueprint.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    users_collection = db['users']
    result = users_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@blueprint.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    users_collection = db['users']
    result = users_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Document Endpoints
@blueprint.route('/documents', methods=['GET'])
def get_documents():
    documents_collection = db['documents']
    documents = list(documents_collection.find())
    return jsonify(documents), 200

@blueprint.route('/documents', methods=['POST'])
def create_document():
    data = request.form
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = uploads.url(filename)
            documents_collection = db['documents']
            document_data = {
                'title': data['title'],
                'summary': data['summary'],
                'file_url': file_url,
                'user_id': data['user_id'],
                'date': datetime.utcnow()
            }
            result = documents_collection.insert_one(document_data)
            # Queue the document for processing asynchronously
            process_document.delay(str(result.inserted_id))
            return jsonify({'message': 'Document created successfully', 'document_id': str(result.inserted_id)}), 201
        except UploadNotAllowed:
            return jsonify({'error': 'File type not allowed'}), 400
    else:
        return jsonify({'error': 'File not allowed'}), 400

@blueprint.route('/documents/<id>', methods=['GET'])
def get_document(id):
    documents_collection = db['documents']
    document = documents_collection.find_one({'_id': ObjectId(id)})
    if document:
        return jsonify(document), 200
    else:
        return jsonify({'error': 'Document not found'}), 404

@blueprint.route('/documents/<id>', methods=['PUT'])
def update_document(id):
    data = request.json
    documents_collection = db['documents']
    result = documents_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Document updated successfully'}), 200
    else:
        return jsonify({'error': 'Document not found'}), 404

@blueprint.route('/documents/<id>', methods=['DELETE'])
def delete_document(id):
    documents_collection = db['documents']
    result = documents_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Document deleted successfully'}), 200
    else:
        return jsonify({'error': 'Document not found'}), 404

# Error Handling
@blueprint.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@blueprint.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@blueprint.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

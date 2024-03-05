from flask import Flask, request, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# SQLite database connection
conn = sqlite3.connect('smart_document_analyzer.db')
c = conn.cursor()

# Create tables if not exist
c.execute('''CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY,
                Username TEXT,
                Password TEXT,
                Email TEXT,
                Role TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS UploadedFiles (
                FileID INTEGER PRIMARY KEY,
                UserID INTEGER,
                FileName TEXT,
                FileType TEXT,
                FileLocation TEXT,
                UploadDateTime TEXT,
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )''')

# Define constants
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define endpoints
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Query the database to check if the user exists
    c.execute('SELECT * FROM Users WHERE Username=? AND Password=?', (username, password))
    user = c.fetchone()

    if user:
        # Successful login
        return jsonify({'message': 'Login successful', 'user_id': user[0]}), 200
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if file is provided
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file type is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Save the uploaded file to the designated folder
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Save file details to the database
    # Assuming UserID is obtained from the authentication process
    user_id = request.form.get('user_id')
    filename_db = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    c.execute('INSERT INTO UploadedFiles (UserID, FileName, FileType, FileLocation) VALUES (?, ?, ?, ?)',
              (user_id, filename, filename.split('.')[-1], filename_db))
    conn.commit()

    return jsonify({'message': 'File uploaded successfully', 'file_name': filename}), 200

if __name__ == '__main__':
    app.run(debug=True)

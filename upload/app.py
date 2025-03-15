
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Set up the upload directory
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for file uploads (optional)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}

def allowed_file(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True

@app.route('/')
def index():
    # Render the HTML upload form
    return render_template_string(open('index.html').read())

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return f'File successfully uploaded: {filename}', 200
    else:
        return 'File type not allowed', 400

if __name__ == '__main__':
    # Bind to all network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)


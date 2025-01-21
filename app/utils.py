import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'data/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    if filename == '':
        raise ValueError("Invalid file name")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

#!/usr/bin/env python
import os
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    g,
    render_template,
    request
)
from werkzeug import secure_filename

UPLOAD_FOLDER = os.getcwd() + '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True # turn this off in production
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ Checks for allowed file extensions
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
           file = request.files['file']
           if file and allowed_file(file.filename):
               filename = secure_filename(file.filename)
               file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
               return render_template('upload.html',
                                       filename=filename)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run()

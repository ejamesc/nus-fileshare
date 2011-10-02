#!/usr/bin/env python
import os, datetime, random
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
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
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_upload_folder(now):
    """ Creates upload folder based on year-month-day
    This is for later use of a cron job to delete folders after a set interval
    """
    newpath = os.path.join(app.config['UPLOAD_FOLDER'],
                        "%s-%s-%s/" % (now.year, now.month, now.day))
    if not os.path.exists(newpath): os.makedirs(newpath)
    return newpath

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Front page view
    """
    if request.method == 'POST':
           file = request.files['file']
           if file and allowed_file(file.filename):
               now = datetime.datetime.now()
               curr_path = create_upload_folder(now)
               filename = secure_filename("%s.%s" % (random.randrange(1,1000000),
                                            file.filename.rsplit('.', 1)[1]))
               file.save(os.path.join(curr_path, filename))
               return render_template('upload.html', filename=filename)
    return render_template('upload.html')


@app.route('/<year>/<month>/<day>/<filename>')
def uploaded_file(year, month, day, filename):
    """ Returns the file based on year, month, date and filename
    Format example: example.com/2011/10/2/234242.gif
    """
    curr_path = os.path.join(app.config['UPLOAD_FOLDER'],
                        "%s-%s-%s/" % (year, month, day))
    return send_from_directory(curr_path, filename)

if __name__ == "__main__":
    app.run()

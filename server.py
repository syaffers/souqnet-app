import os
import random
from flask import (
    Flask, flash, render_template, redirect, request, send_from_directory,
    session, url_for,
)
from werkzeug.utils import secure_filename

LETTER_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
UPLOAD_FOLDER = '/tmp/souqnet-app/'
ALLOWED_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def random_name(fn):
    ext = fn.split('.')[-1]
    rns = [random.randint(0, len(LETTER_SET)) for _ in range(3)]
    name = ''.join([LETTER_SET[rn] for rn in rns])
    return "{new_fn}.{ext}".format(new_fn=name, ext=ext)


def allowed_file(filename):
    allowed_ext = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return '.' in filename and allowed_ext


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # show the upload form
        return render_template('home.html')

    if request.method == 'POST':
        # check is file is passed into the POST
        if 'image' not in request.files:
            flash('No file was uploaded.')
            return redirect(request.url)

        # if filename is empty, then users didn't upload anythin
        image_file = request.files['image']
        if image_file.filename == '':
            flash('No selected file.')
            return redirect(request.url)

        # check if the file is "legit"
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(random_name(image_file.filename))
            image_file.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename)
            )
            return redirect(url_for('predict', filename=filename))


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/predict/<filename>')
def predict(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

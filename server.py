import os

from numpy import stack
from imageio import imread
from keras.models import load_model
from flask import (Flask, flash, render_template, redirect, request, session,
                   send_file, url_for)
from werkzeug.utils import secure_filename

from utils import generate_barplot, random_name

ALLOWED_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg', 'gif'])
NEURAL_NET_MODEL_PATH = os.environ['NEURAL_NET_MODEL_PATH']

NEURAL_NET = load_model(NEURAL_NET_MODEL_PATH)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']


def allowed_file(filename):
    """ Checks if a filename's extension is acceptable """
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
    """ Route for error page """
    return render_template('error.html')


@app.route('/images/<filename>')
def images(filename):
    """ Route for serving uploaded images """
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/predict/<filename>')
def predict(filename):
    """ After uploading the image, show the prediction of the uploaded image
    in barchart form
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_mtx = imread(filepath)
    image_mtx = image_mtx.astype(float) / 255.

    try:
        # HACK: imageio seems to automatically infer grayscale images as a
        # 2d tensor, not 3d; need to support this logic. For now just duplicate
        # the first channel.
        image_mtx = image_mtx[:, :, :3]
    except IndexError:
        image_mtx = stack((image_mtx, image_mtx, image_mtx), axis=2)

    try:
        # HACK: Reshape for neural net input, redirect to error page if input
        # image is not 128x128
        image_mtx = image_mtx.reshape(-1, 128, 128, 3)
    except ValueError:
        return redirect(url_for('error'))

    # TODO: Celery defer this as it may take some time
    predictions = NEURAL_NET.predict_proba(image_mtx)
    # TODO: Barplots with hover functionality
    script, div = generate_barplot(predictions)

    return render_template(
        'predict.html',
        plot_script=script,
        plot_div=div,
        image_path='/images/{}'.format(filename)
    )

# SouqNet Web Application

## Setting Up

Create a new environment using the `requirements.txt` file:

    $ conda create --name <env> --file requirements.txt


Set the Keras trained neural network path in `server.py`:

    NEURAL_NET_MODEL_PATH = os.environ['NEURAL_NET_MODEL_PATH']
    # or
    NEURAL_NET_MODEL_PATH = "/models/SouqNet128v2_gpu.h5"


Set a secret key (since Flask needs this when posting forms) in `server.py`:

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # or
    app.config['SECRET_KEY'] = "SOMEreallyR@ND0M5TR1NGtoK33pYouSeKYUR"


Set an upload folder path in `server.py`:

    app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
    # or
    app.config['UPLOAD_FOLDER'] = "/tmp/souqnet/"


## Running

Use the following command prefaced by the `FLASK_APP` setting

    $ FLASK_APP=server.py flask run

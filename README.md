# SouqNet Web Application

## Setting Up

Create a new environment using the `requirements.txt` file:

    $ conda create --name <env> --file requirements.txt
    ... (some output messages)

Set the Keras trained neural network path in `server.py`:

    NEURAL_NET_MODEL_PATH = os.environ['NEURAL_NET_MODEL_PATH']
    # or
    NEURAL_NET_MODEL_PATH = "/path/to/models/SouqNet128v2_gpu.h5"

Set a secret key (since Flask needs this when posting forms) in `server.py`:

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # or
    app.config['SECRET_KEY'] = "SOMEreallyR@ND0M5TR1NGtoK33pYouSeKYUR"

Set an upload folder path in `server.py`. `/tmp/` folders will delete all
uploaded images:

    app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
    # or
    app.config['UPLOAD_FOLDER'] = "/tmp/souqnet/"

## Running

Use the following command prefaced by the `FLASK_APP` setting

    $ FLASK_APP=server.py flask run
    ... (some output messages)

## Related article

An article was originally posted on March 26, 2018 in tandem with this repository to explain how the app was built. The original article can be view on [StackSchool.io][1]. In efforts to keep the article alive on the internet, the article is reuploaded into this repository under the `ARTICLE.md` file.

[Read the article...](ARTICLE.md)

[1]: http://stackschool.io/quick-image-classifier-web-application-with-flask-keras-and-bokeh/

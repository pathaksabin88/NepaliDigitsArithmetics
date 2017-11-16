import os
from os.path import join, dirname, realpath

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path="", static_folder = "templates/images")

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'templates/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputImage']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', img=file.filename)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def helpPage():
    return render_template('help.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run()

import os
import shutil
from os.path import join, dirname, realpath

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from bodmasCalculation import getStringWithoutSpaceFromList
from performAction import *
from processImage import apply_threshold

app = Flask(__name__, static_folder="static")

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploadedImages/')
FOLDER_UPLOADED_IMAGES = join(dirname(realpath(__file__)), 'static/uploadedImages')
FOLDER_CHARACTER_CSV = join(dirname(realpath(__file__)), 'static/characterCsv')
FOLDER_SEGMENTED_IMAGES = join(dirname(realpath(__file__)), 'static/segmentedImages')
FOLDER_DIGIT_SEGMENTED_IMAGES = join(dirname(realpath(__file__)), 'static/digitSegmentedImages')
FOLDER_PROCESSED_IMAGES = join(dirname(realpath(__file__)), 'static/processedImages')
FOLDER_OUTPUT = join(dirname(realpath(__file__)), 'static/output')
FOLDER_OUTPUT_IMAGES = join(dirname(realpath(__file__)), 'static/outputImages')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def deleteAllProcessedImages():
    shutil.rmtree(FOLDER_PROCESSED_IMAGES)
    os.mkdir(FOLDER_PROCESSED_IMAGES)


def deleteAllSegmentedImages():
    shutil.rmtree(FOLDER_SEGMENTED_IMAGES)
    os.mkdir(FOLDER_SEGMENTED_IMAGES)


def deleteAllDigitSegmentedImages():
    shutil.rmtree(FOLDER_DIGIT_SEGMENTED_IMAGES)
    os.mkdir(FOLDER_DIGIT_SEGMENTED_IMAGES)


def deleteAllCsvData():
    shutil.rmtree(FOLDER_CHARACTER_CSV)
    os.mkdir(FOLDER_CHARACTER_CSV)


def deleteAllOutputImages():
    shutil.rmtree(FOLDER_OUTPUT_IMAGES)
    os.mkdir(FOLDER_OUTPUT_IMAGES)


def deleteOutputImage():
    shutil.rmtree(FOLDER_OUTPUT)
    os.mkdir(FOLDER_OUTPUT)


def deleteUploadedImages():
    shutil.rmtree(FOLDER_UPLOADED_IMAGES)
    os.mkdir(FOLDER_UPLOADED_IMAGES)


def deleteAllUsedImages():
    deleteAllProcessedImages()
    deleteAllSegmentedImages()
    deleteAllDigitSegmentedImages()
    deleteAllCsvData()
    deleteAllOutputImages()
    deleteOutputImage()


@app.route('/', methods=['GET', 'POST'])
def index():
    deleteUploadedImages()
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputImage']
    # output_filename = ''
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        print(UPLOAD_FOLDER + file.filename)
        # shutil.rmtree(FOLDER_PROCESSED_IMAGES)
        # os.mkdir(FOLDER_PROCESSED_IMAGES)
        # print("All Files Deleted!")
        deleteAllUsedImages()
        characters_img = image_processing(filename)
        recognized_characters_list = recognition_character(characters_img)
        output_filename = writing_final_solution(recognized_characters_list)
        if not output_filename:
            recognized_exp_string = getStringWithoutSpaceFromList(recognized_characters_list)
            return render_template('error.html', recognized_exp_string=recognized_exp_string)
        else:
            return render_template('index.html', inputimg='uploadedImages/' + file.filename,
                                   out='output/' + output_filename)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def helpPage():
    return render_template('help.html')


@app.route('/error', methods=['GET', 'POST'])
def errorPage():
    return render_template('error.html')


@app.route('/completeSolution', methods=['GET', 'POST'])
def completeSolution():
    input_images = os.listdir(FOLDER_UPLOADED_IMAGES)
    processed_images = os.listdir(FOLDER_PROCESSED_IMAGES)
    print(processed_images)
    segmented_images = os.listdir(FOLDER_SEGMENTED_IMAGES)
    print(segmented_images)
    digit_segmented_images = os.listdir(FOLDER_DIGIT_SEGMENTED_IMAGES)
    print(digit_segmented_images)
    output_images = os.listdir(FOLDER_OUTPUT_IMAGES)
    print(output_images)
    return render_template('completeSolution.html', input_images=input_images, processed_images=processed_images,
                           segmented_images=segmented_images, digit_segmented_images=digit_segmented_images,
                           output_images=output_images)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)

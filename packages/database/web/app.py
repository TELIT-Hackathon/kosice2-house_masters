from flask import Flask
from flask import jsonify
from flask import send_file

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Hi, World!'


@app.route('/try', methods=['GET', 'POST'])
def analyze_frame(frame):
    a = {
        "free_parking_spots": frame["a"],
        "number_of_parking_spots": frame["nops"],
        "cars_detected:": frame["cd"]
    }
    return jsonify(a)


@app.route('/endpoint', methods=['GET', 'POST'])
def test_analyze_endpoint():
    frame = {
        "a": 4,
        "nops": 20,
        "cd": 7
    }
    return analyze_frame(frame)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadPhoto', methods=['GET', 'POST'])
def upload_file():
    print(app.config)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return "success"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/returnPhoto', methods=['GET', 'POST'])
def test_return_photo():
    filename = 'images/test_img3.png'
    return send_file(filename, mimetype='image/gif')
    # return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=1)

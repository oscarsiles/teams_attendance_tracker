import os
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import csv
from io import StringIO 

from app.attendance import calculate_attendance

UPLOAD_FOLDER = 'app/uploads/'

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":

        # check if the post request has the file part
        if 'csvfile' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['csvfile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(df)
            result = calculate_attendance(df)
            result.to_csv(UPLOAD_FOLDER + "[ATTENDANCE]" + filename, index=False)
            #Delete file from storage after creating dataframe
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('data.html')


# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    print("DELETED")
    return send_file(file_path, as_attachment=True, attachment_filename='')


# if __name__ == "__main__":
#     app.run(debug=True)
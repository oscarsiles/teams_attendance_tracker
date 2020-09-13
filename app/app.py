import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import csv
from io import StringIO 
from datetime import datetime

from app.attendance import calculate_attendance

UPLOAD_FOLDER = './app/uploads/'
result_copy = ['HELLO']

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/data", methods=["GET", "POST"])
def data():
    
    if request.method == "POST":
        time_format = '%Y-%m-%dT%H:%M'
        start_time = datetime.strptime(request.form['start_time'], time_format)
        end_time = datetime.strptime(request.form['end_time'], time_format)
        print(f'Edited  Time: {start_time} -- {end_time}')
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
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(df)
            # start_time = df['Timestamp'].iloc[0]
            # print(start_time)
            result = calculate_attendance(df, start_time, end_time)
            result_copy = result
            print(f'RESULT COPY 1: {result_copy}')
            result.to_csv(UPLOAD_FOLDER + "[ATTENDANCE]" + filename, index=False)
            #Delete file from storage after creating dataframe
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #send file name as parameter to downlad
            return redirect(url_for('download_file', filename=filename))
    return render_template('data.html')


# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    print(f'RESULT COPY: {result_copy}')
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


# if __name__ == "__main__":
#     app.run(debug=True)
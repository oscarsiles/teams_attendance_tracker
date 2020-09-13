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
        if 'attendance-file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['attendance-file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:

            filename = secure_filename(file.filename)
            print(f'hi FILENAME: {filename}')
            #get file extension
            file_extension = os.path.splitext(filename)[1]

            #save file to uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if file_extension == '.csv':
            #read file as pandas dataframe considering file extension
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            elif file_extension == '.xlsx':
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            else:
                return "Unsupported file type please upload .csv or .xlsx file"
            print(df)
            
            #calculate time attended and return a dataframe
            result = calculate_attendance(df, start_time, end_time)

            #copy result dataframe
            result_copy = result
            print(f'RESULT COPY 1: {result_copy}')

            #convert result dataframe to .csv file for user to download
            result.to_csv(UPLOAD_FOLDER + "[ATTENDANCE]" + filename, index=False)

            #Delete file from storage after creating dataframe
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #send file name as parameter to downlad
            return redirect(url_for('download_file', filename=filename))
    return render_template('data.html')


# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    print("Result Copy:")
    print(result_copy)
    print(f'Filename: {filename}')
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


# if __name__ == "__main__":
#     app.run(debug=True)
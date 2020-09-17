import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import csv
from io import StringIO 
from datetime import datetime

from app.attendance import calculate_attendance

UPLOAD_FOLDER = './app/uploads/'

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/data", methods=["GET", "POST"])
def data():
    
    if request.method == "POST":
        #Time Format for Chrome
        time_format = '%Y-%m-%dT%H:%M'

        #Convert time from html to python datetime.
        start_time = datetime.strptime(request.form['start_time'], time_format)
        end_time = datetime.strptime(request.form['end_time'], time_format)
        print(f'Edited  Time: {start_time} -- {end_time}')

        #Get file uploaded by user
        file = request.files['attendance-file']
        filename = secure_filename(file.filename)
        print(f'FILENAME: {filename}')
        #get file extension
        file_extension = os.path.splitext(filename)[1]
        filename_without_extension = os.path.splitext(filename)[0]

        #save file to uploads folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #read file as pandas dataframe considering file extension
        if file_extension == '.csv':
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif file_extension == '.xlsx':
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        else:
            return "Unsupported file type please upload .csv or .xlsx file"
        print(df)
        
        #calculate time attended and return a dataframe
        result = calculate_attendance(df, start_time, end_time)
        result_copy = result
        #convert result dataframe to .csv file for user to download
        result_filename = "[ATTENDANCE]" + filename_without_extension + ".csv"
        result.to_csv(UPLOAD_FOLDER + result_filename, index=False)

        #Delete file from storage after creating dataframe
        # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #send file name as parameter to downlad
        # return redirect(url_for('download_file', filename=filename, result=result_copy))
        return render_template('download.html', file_chosen=file_chosen, value=result_filename, result=result.to_html())

    return render_template('data.html')


#Download demo file 'test.csv'
@app.route('/demo.csv')
def download_demo_file():
    demo_file_path = 'uploads/test.csv'
    return send_file(demo_file_path, as_attachment=False, attachment_filename='test.csv')
    
# @app.route('/view-file')
# def view_file():

#     print(f'DATAFRAME: {df}')
#     return render_template('index.html', original_file=df)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request
import pandas as pd
import csv
from io import StringIO 

from attendance import calculate_attendance

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        f = request.files['csvfile']
        print(f'--------> {f}')
        data = []
        data = f.read().decode("utf-8")

        StringData = StringIO(data)
        df = pd.read_csv(StringData)
        print(df)

        result = calculate_attendance(df)

        return render_template('data.html', data=result)

if __name__ == "__main__":
    app.run(debug=True)
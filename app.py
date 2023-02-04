from calendar import month_name
from flask import Flask, render_template, request, send_file, send_from_directory, Response, flash, redirect
import pandas as pd
from demand import *
import os
from collections import deque


app = Flask(__name__)

app.config['DOWNLOAD_FOLDER'] = 'Results'
app.secret_key = os.urandom(12)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


d = {}


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':

        #file = request.form['file']
        file = request.files['file']
        file.save(file.filename)

        Annual_demand = int(request.form['Annual_demand'])

        data = Demand_Planning(file, Annual_demand)

        global d

        d['monthly_demand'] = data[1]
        data = data[0]

        d['file'] = file.filename
        d['data'] = data
        d['Annual_demand'] = data

        #data = Route_Optimization(file,Plant_demand, IS_demand, RB_CB_Ratio, MBR_percentage)

        #data = pd.read_excel('result.xlsx')
        titles = data.columns.values
        rows = [list(data[i].values) for i in titles]
        length = len(data)
        data = data.T
        row0 = data.columns.values
        rows.insert(0, row0)
        rows = np.array(rows).T.tolist()
        data = data.T
        name = 'annual_demand'

        return render_template('data.html', name=name, rows=rows, titles=data.columns.values, length=length)

    else:

        data = d['Annual_demand']
        titles = data.columns.values
        rows = [list(data[i].values) for i in titles]
        length = len(data)
        data = data.T
        row0 = data.columns.values
        rows.insert(0, row0)
        rows = np.array(rows).T.tolist()
        data = data.T
        name = 'annual_demand'

        return render_template('data.html', name=name, rows=rows, titles=data.columns.values, length=length)


@app.route('/ex_monthly_demand', methods=['GET', 'POST'])
def data2():

    global d

    file = d['file']
    data = d['data']
    data = data.T

    Plant_demand = int(data['Monthly Demand'][0])  # in cb terms

    data = Route_Optimization(file, Plant_demand)
    d['alloc'] = data[1]
    d['MBR_stakeholders'] = data[2]
    d['remaining_plant_demand'] = data[3]
    data = data[0]
    d['result_combinations'] = data

    titles = data.columns.values
    rows = [list(data[i].values) for i in titles]
    rows = np.array(rows).T.tolist()
    length = len(data)
    name = 'monthly_demand'

    return render_template('data.html', name=name, rows=rows, titles=data.columns.values, length=length)


@app.route('/download', methods=['GET', 'POST'])
def download():

    filename = 'result.xlsx'

    excelDownload = open(filename, 'rb').read()

    return Response(
        excelDownload,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-disposition":
                 "attachment; filename=result.xlsx"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)

#Script python

from flask import Flask, render_template, request
import pandas as pd 
import csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import locale

app = Flask(__name__)
app.run(debug = True)
@app.route('/')
def student():

   return render_template('form4.html')

@app.route('/', methods=['POST'])
def my_form_post():
	# get data from html form
    tahun = int(request.form['tahun'])
    kapasitas = int(request.form['kapasitas'])
    biayagantioli = int(request.form['gantioli'])
    turbo = request.form['turbo']
    jenis = request.form['jenis']

    if turbo == 'NA':
        t = 0
    else:
        t = 1

    if jenis == 'MPV':
        j = 0
    elif jenis == 'Hatchback':
        j = 1
    else:
        j = 2

    data = pd.read_csv('cardatanum.csv', index_col = 0)
    c=['Year','Displacement', 'Turbo', 'OilChangeCost', 'Category']
    df = data[c]
    y=data['MarketPrice']

    x_train,x_test,y_train,y_test=train_test_split(df,y,train_size=0.8,random_state=42)
    reg=LinearRegression()
    reg.fit(x_train,y_train)
    a = reg.predict([[tahun, kapasitas, t, biayagantioli, j]])[0]
    s = '{:,}'.format(int(a)).replace(',','.')
    out = "<h1>Preferensi</h1><br>Tahun:" + str(tahun) + "<br>" + "Displacement: " + str(kapasitas) + "<br>"
    out = out + "Biaya ganti oli Rp. " + str(biayagantioli) + "<br>Turbo: " + turbo + "<br>"
    out = out + "Kategori: " + jenis + "<br>"
    s = out + "<h2>Prediksi harga: Rp. " + s + "</h2>"

    return s


if __name__ == '__main__':
   app.run(debug = True)
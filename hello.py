#Script python

from flask import Flask, render_template, request
import pandas as pd 
import csv

app = Flask(__name__)
app.run(debug = True)
@app.route('/')
def student():

   return render_template('form3.html')

@app.route('/', methods=['POST'])
def my_form_post():
	# get data from html form
    tahunmin = int(request.form['tahunmin'])
    tahunmax = int(request.form['tahunmax'])
    bbm = request.form['bbm']
    kapasitasmin = int(request.form['kapasitasmin'])
    kapasitasmax = int(request.form['kapasitasmax'])
    biayagantioli = float(request.form['gantioli'])
    jenis = request.form['jenis']

    hargamax = float(request.form['hargamax'])

    # read csv from original file
    data = pd.read_csv('cardata.csv', index_col = 0)

    minyear = data.Year >= tahunmin
    maxyear = data.Year <= tahunmax
    mincap = data.Displacement >= kapasitasmin
    maxcap = data.Displacement <= kapasitasmax
    oilcost = data.OilChangeCost <= biayagantioli
    fuel = data.Fuel == bbm
    marketprice = data.MarketPrice <= hargamax
    catfilter = data.Category == jenis

    dfList = data['OilChangeCost'].tolist()
    prior = [abs(x-biayagantioli) for x in dfList]
    data.insert(loc=10, column='Prior', value=prior)

    #filtering data based on user preferences

    if jenis == "any":
        userpref = minyear & maxyear & mincap & maxcap & oilcost & marketprice & fuel
    else:
        userpref = minyear & maxyear & mincap & maxcap & oilcost & marketprice & fuel & catfilter


    #ranking berdasarkan (1) oilcost similarity (2) fuel economy (3) displacement
    # data[userpref].sort_values(by = ['FuelEconomy', 'Displacement'], ascending = [True, False]).to_csv('out.csv', index = False, encoding='utf8')

    df = data[userpref].sort_values(by = ['Prior','FuelEconomy', 'MarketPrice'], ascending = [True, False, False]).assign()

    df.head(10).to_csv('out.csv', index = False, encoding='utf8')
    
    #Show data results 
    s = "<h1>Preferensi</h1>Tahun: " + str(tahunmin)+" - " + str(tahunmax) + "<br> Bahan bakar: " + bbm
    s = s + "<br> Kapasitas Mesin: " + str(kapasitasmin) + " - " + str(kapasitasmax)
    s = s + "<br> Biaya ganti oli (maks): Rp. " + str(biayagantioli) + "<br> Harga (maks): Rp. " + str(hargamax)

    s = s + "<h1>Rekomendasi</h1>"
    
    # begin the table
    s = s + "<table border = 1>"
    # column headers
    #                             0            1             2                 4
    s = s + "<tr><th>No</th><th>Type</th><th>Jenis</th><th>Tahun</th> <th>BBM</th> <th>Displacement</th>"
    s = s + "<th>Oil Change Cost</th> <th>Market Price</th>"
    s = s + "</tr>"

    no = 0
    with open('out.csv') as csvfile:
    	rows = csv.reader(csvfile, delimiter=',')
    	for row in rows:
            no = no + 1
            # no header
            if no > 1:
                s = s + "<tr>"
                s = s + "<td>"+ str(no-1) + "</td>" 
                s = s + "<td>"+row[0] + "</td>"  #type
                s = s + "<td>"+row[8] + "</td>" #jenis
                s = s + "<td>"+row[1] + "</td>"  #tahun
                s = s + "<td>"+row[2] + "</td>"  #bbm
                s = s + "<td>"+row[3] + "</td>" 
                s = s + "<td>"+row[5] + "</td>" 
                s = s + "<td>"+row[9] + "</td>" 
                s = s + "</tr>"

    s = s + "</table>"
    return s


if __name__ == '__main__':
   app.run(debug = True)
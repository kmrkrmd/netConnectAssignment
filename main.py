from flask import *
import pandas as pd
import sqlite3
import requests
conn = sqlite3.connect("gdpData.db")
df = pd.read_csv('GDP Data.csv')
for i in range(len(df['Year'])):
    cur=conn.execute("SELECT * FROM gdp WHERE year=?",(df['Year'][i],))
    if cur.fetchone() == None:
        conn.execute("INSERT INTO gdp(year,price)VALUES(?,?)",(df['Year'][i],df['Price'][i]))
        conn.commit()
    else:
        conn.execute("UPDATE gdp SET price=? WHERE year=?",(df['Price'][i],df['Year'][i]))
        conn.commit()
app = Flask(__name__)
@app.route('/')
def index():
    conn = sqlite3.connect("gdpData.db")
    cur = conn.execute("SELECT * FROM gdp")
    rows1 = cur.fetchall()
    r2=[]
    r3=[]
    for i in rows1:
        r2.append(int(i[1].replace('*','')))
        r3.append(float(i[2].replace(',','')))

    return render_template("index.html",rows1=r2,rows2=r3,n=len(r2))
@app.route('/convert')
def currency_converter():
    url1 = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=fce74ac816df45d5a2ce2785b9d0dc66"
    r=requests.get(url=url1)
    data = r.json()
    conn = sqlite3.connect("gdpData.db")
    cur = conn.execute("SELECT * FROM gdp")
    rows1 = cur.fetchall()
    r2 = []
    r3 = []
    for i in rows1:
        r2.append(int(i[1].replace('*', '')))
        r3.append(round((float(i[2].replace(',', '')) * float(data["rates"]["INR"])),2))
    return render_template("index.html", rows1=r2, rows2=r3, n=len(r2))



if __name__ == "__main__":
    app.run()
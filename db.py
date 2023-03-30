import sqlite3
conn=sqlite3.connect("gdpData.db")
#conn.execute("CREATE TABLE gdp(id INTEGER PRIMARY KEY AUTOINCREMENT,year TEXT,price TEXT)")
cur = conn.execute("SELECT * FROM gdp")
print(cur.fetchall())
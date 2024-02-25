import sqlite3
import constVaribel
def read():
    conn = sqlite3.connect(constVaribel.database)
    c = conn.cursor()

    c.execute("SELECT * FROM tracks")

    rows = c.fetchall

    for k in rows:
        print(k)

    conn.close()

print("Starting")
read()
print("Table is read")
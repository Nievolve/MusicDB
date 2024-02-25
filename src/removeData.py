import sqlite3
import constVaribel
def remove():
    conn = sqlite3.connect(constVaribel.database)

    cursor = conn.cursor()
#Table remains but ALL data i wiped
    cursor.execute("DELETE FROM tracks")

    conn.commit()

    conn.close()

print("Starting")
remove()
print("Data is removed")
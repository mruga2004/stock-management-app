import sqlite3

con = sqlite3.connect("ims.db")
cur = con.cursor()

cur.execute("UPDATE sales SET date = '2024-04-01 00:00:00' WHERE sid = 4")
cur.execute("UPDATE sales SET date = '2024-06-15 00:00:00' WHERE sid = 5")
cur.execute("UPDATE sales SET date = '2024-09-10 00:00:00' WHERE sid = 6")
cur.execute("UPDATE sales SET date = '2025-01-20 00:00:00' WHERE sid = 7")
cur.execute("UPDATE sales SET date = '2025-03-30 00:00:00' WHERE sid = 8")

con.commit()
con.close()
print("Dates updated successfully!")

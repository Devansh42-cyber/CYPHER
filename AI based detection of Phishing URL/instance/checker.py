import sqlite3

conn = sqlite3.connect("app.db")
c = conn.cursor()

# show all users
rows = c.execute("SELECT * FROM user").fetchall()

if rows:
    for r in rows:
        print(r)
else:
    print("No users found.")

conn.close()

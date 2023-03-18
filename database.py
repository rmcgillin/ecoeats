import sqlite3

#connect to db
conn = sqlite3.connect('EcoEats Database.db')

#create a cursor
cursor = conn.cursor()

#

cursor.execute('SELECT * FROM users')

cursor.close()
conn.close()

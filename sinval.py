import sqlite3
import time

# Open the main content (Read only)
conn = sqlite3.connect('file:stars.sqlite?mode=ro', uri=True)
cur = conn.cursor()

print('Checking for invalid information.....')
time.sleep(1)

#Count Invalid data
cur.execute('SELECT COUNT(invalid) FROM Stars WHERE invalid=1')
row=cur.fetchone()
inv=row[0]

#Count NULL columns
cur.execute('SELECT COUNT(CASE WHEN mag IS NULL THEN 1 END) FROM Stars')
row=cur.fetchone()
nul=row[0]

#Count All
cur.execute('SELECT COUNT() FROM Stars')
row=cur.fetchone()
all=row[0]

print('Invalid stars:', inv+nul)
print(round((inv+nul)/all*100,3), end="")
print('% of all data')

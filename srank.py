import sqlite3

# Open the main content (Read only)
conn = sqlite3.connect('file:stars.sqlite?mode=ro', uri=True)
cur = conn.cursor()

while True :
    rank=input('Rank by brightest (B) or faintest (F) stars?')
    if len(rank) < 1:
        quit()
    if rank == 'B' or rank == 'b' :
        cur.execute('SELECT id,mag,invalid FROM Stars ORDER BY mag ASC')
        break
    if rank == 'F' or rank == 'f' :
        cur.execute('SELECT id,mag,invalid FROM Stars ORDER BY mag DESC')
        break
    print('Invalid input. Please enter either \'B\' or \'F\'')

while True :
    top=input('How many stars to rank? ')
    if len(top) < 1:
        quit()
    try:
        top=int(top)
        break
    except:
        print('Please enter a valid number.')
        continue

row=cur.fetchone()
count= 0
print('')

while top > count :
    id=row[0]
    mag=row[1]
    inv=row[2]
    if mag is None or inv == 1 :
        row=cur.fetchone()
        continue
    #print(row)
    count=count+1
    print(count,end="")
    print('º: Star HD',id, end="")
    print('; mag =', mag)
    row=cur.fetchone()
    

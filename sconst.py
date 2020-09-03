import sqlite3

# Open the main content (Read only)
conn = sqlite3.connect('file:stars.sqlite?mode=ro', uri=True)
cur = conn.cursor()

while True :
    many = input('How many constellations to rank? (max for all)')
    if len(many)<1 :
        quit()
    try :
        if many == 'max' or many == 'MAX':
            cur.execute('SELECT COUNT() FROM Constellations')
            row=cur.fetchone()
            many=row[0]
            break
        cur.execute('SELECT COUNT() FROM Constellations')
        row=cur.fetchone()
        many=int(many)
        if many > row[0] :
            print('Number of constellations specified above number of valid records (', end="")
            print(row[0],end="")
            print('). Please enter a lower number.')
            continue
        break
    except:
        print('Please enter a valid number')
        continue

while True :
    stars = input('How many Stars to consider (starting from HD1)? (max for all)')
    if len(stars)<1 :
        quit()
    try:
        if stars == 'max' or stars == 'MAX':
            cur.execute('SELECT COUNT() FROM Stars WHERE invalid=0 AND mag IS NOT NULL')
            row=cur.fetchone()
            stars=row[0]
            break
        stars=int(stars)
        cur.execute('SELECT COUNT() FROM Stars WHERE invalid=0 AND mag IS NOT NULL')
        row=cur.fetchone()
        if stars > row[0] :
            print('Number of stars specified above number of valid records (', end="")
            print(row[0],end="")
            print('). Please enter a lower number.')
            continue
        break
    except:
        print('Please enter a valid value')
        continue

cur.execute('''SELECT Stars.id, mag, invalid, const FROM Stars JOIN Constellations ON Stars.const_id=Constellations.id
            WHERE Stars.invalid=0 AND Stars.mag IS NOT NULL''')

row=cur.fetchone()
#print(row)
const=dict()
count=1

while stars > count :
    const[row[3]]=const.get(row[3],0)+1
    count=count+1
    row=cur.fetchone()

const_sort=sorted(const.items(), key=lambda x: x[1], reverse=True)

#Count constellations recovered and print results
i=0
lst=list()

for tup in const_sort :
    val=tup[0]+': '+str(tup[1])+' stars'
    lst.append(val)
    if i==many :
        break
    i=i+1

print('')
if i != many :
    print('Not enough stars to rank', many, 'constellations')

print(stars, 'stars analyzed. Recovered', i, 'constellations.' )
print('Top', i, 'constellations:')

j=1
for con in lst :
    print('\t',j, end="")
    print('º',con)
    j=j+1

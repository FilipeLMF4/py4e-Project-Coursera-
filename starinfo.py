import sqlite3
import xml.etree.ElementTree as ET
import time

conn=sqlite3.connect('stars.sqlite')
cur=conn.cursor()

# Open the main content (Read only)
conn_1 = sqlite3.connect('file:starxml.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

cur_1.execute('SELECT max(id) FROM Stars_Raw')
max=cur_1.fetchone()
last=max[0]
#print(last)

while True :
    ag=input('Start from scratch (Y/N)? ')
    if len(ag) < 1:
        quit()
    if ag == 'Y' or ag == 'y' or ag == 'N' or ag == 'n' :
        break
    else :
        print('Invalid command. Please try again.')
        continue

#Restart process
if ag == 'Y' or ag == 'y' :
    cur.execute('DROP TABLE IF EXISTS Stars')
    cur.execute('DROP TABLE IF EXISTS Constellations')
    while True :
        val=input('How many stars to process? (max for all)')
        if len(val) < 1:
            quit()
        try :
            if val == 'max' or val == 'MAX' :
                many=last
            else :
                many=int(val)
            break
        except:
            print('Please enter a valid number')
            continue
    starID = 1

if len(ag) < 1:
    quit()

cur.execute('''CREATE TABLE IF NOT EXISTS Stars
    (id INTEGER UNIQUE, ra INTEGER, dec INTEGER, mag INTEGER, const_id INTEGER, invalid INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Constellations
    (id INTEGER UNIQUE, const TEXT UNIQUE)''')

count = 0
err=0

#Pick up where we left off
if ag == 'N' or ag == 'n':
    while True :
        val=input('How many stars to process? (max for all)')
        if len(val) < 1:
            quit()
        try:
            if val == 'max' or val == 'MAX' :
                break
            many=int(val)
            break
        except:
            print('Please enter a valid number')
            continue

    cur.execute('SELECT max(id) FROM Stars' )
    try:
        row = cur.fetchone()
        if row is None :
            starID = 1
        else :
            starID = row[0]

    except:
        starID = 1

    if starID == last :
        print('All stars already processed! Quitting...')
        quit()

    if starID == None :
        starID = 1

    if val == 'max' :
        many = last-starID

    print('Restarting process from star HD', starID)

if ag=='y' or ag == 'Y' :
    cur_1.execute('SELECT id,xml FROM Stars_Raw WHERE id >= ? ORDER BY id LIMIT ?', (starID,many))
else :
    cur_1.execute('SELECT id,xml FROM Stars_Raw WHERE id >= ? ORDER BY id LIMIT ?', (starID+1,many))

bad=list()
inval=list()

for star in cur_1 :
    xml=star[1]
    try :
        elem=ET.fromstring(xml)

    except:
        print('Data missing for star HD', star[0])
        cur.execute('INSERT OR IGNORE INTO Stars (id, ra, dec, mag, const_id, invalid) VALUES (?,NULL,NULL,NULL,NULL,0)',(star[0],))
        conn.commit()
        bad.append(star[0])
        count=count+1
        continue

    obj=elem.findall('object')

    #Get Values
    for child in obj:
        #Constellation
        const=child.find('constellation')
        constname = const.text
        constid = const.get('id')

        #Coordinates
        rah=child.find('ra').text
        dedeg=child.find('de').text

        #Magnitude
        mag=child.find('mag').text

    #Conversion
    try:
        mag=float(mag)
        rah=float(rah)
        dedeg=float(dedeg)
        constid=int(constid)
    except:
        print('Invalid data on star HD', star[0])
        cur.execute('INSERT OR IGNORE INTO Stars (id, ra, dec, mag, const_id, invalid) VALUES (?,?,?,?,?,1)',(star[0],rah,dedeg,mag,constid))
        conn.commit()
        inval.append(star[0])
        count=count+1
        continue

    try :
        cur.execute('INSERT OR IGNORE INTO Stars (id, ra, dec, mag, const_id, invalid) VALUES (?,?,?,?,?,0)',(star[0],rah,dedeg,mag,constid))
        cur.execute('INSERT OR IGNORE INTO Constellations (id, const) VALUES (?,?)', (constid, constname))
        conn.commit()

    except KeyboardInterrupt :
        err=1
        print('\n\rProcess interrupted by User ...')
        print('Last star processed: HD', star [0])
        print(len(inval), 'stars with invalid data.')
        print(len(bad), 'stars with missing data.',end="")
        if len(bad)>=1 or len(inval)>=1:
            badlist = input('"S" for list or Enter to exit.')
            if badlist == 'S' or badlist == 's' :
                print('\n\rMissing data:',bad)
                print('\n\rInvalid data:',inval)
        break

    count=count+1

    if count == 1 :
        print('Processing... (',end="")
        print(count, end="")
        print('/',end="")
        print(many,end="")
        print(')')

    if count%100 == 0 or count==many:
        print('Processing... (',end="")
        print(count, end="")
        print('/',end="")
        print(many,end="")
        print(')')

    #print(constid, constname, rah, dedeg, mag)

if err != 1 :
    print('\r\nData processing successful')
    print('Last star processed: HD', star [0])
    print(len(inval), 'stars with invalid data.')
    print(len(bad), 'stars with missing data.',end="")
    if len(bad)>=1 or len(inval)>=1:
        badlist = input('"S" for list or Enter to exit.')
        if badlist == 'S' or badlist == 's' :
            print('\n\rMissing data:',bad)
            print('\n\rInvalid data:',inval)

cur_1.close()
cur.close()

import sqlite3
import xml.etree.ElementTree as ET
import time

conn=sqlite3.connect('stars.sqlite')
cur=conn.cursor()

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
    val=input('How many stars to clean? ')
    while True :
        val=input('How many stars to clean? ')
        if len(val) < 1:
            quit()
        try :
            many=int(val)+1
            break
        except:
            print('Please enter a valid number')
            continue
    starID = 1

if len(ag) < 1:
    quit()

cur.execute('''CREATE TABLE IF NOT EXISTS Stars
    (id INTEGER UNIQUE, ra TEXT, dec TEXT, mag INTEGER, const_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Constellations
    (id INTEGER UNIQUE, const TEXT UNIQUE)''')

count = 0
err=0

# Open the main content (Read only)
conn_1 = sqlite3.connect('file:starxml.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

#Pick up where we left off
if ag == 'N' or ag == 'n':
    while True :
        val=input('How many stars to clean? ')
        if len(val) < 1:
            quit()
        try :
            many=int(val)+1
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

    if starID == None :
        starID = 1

    print('Restarting process from star HD', starID)

cur_1.execute('SELECT id,xml FROM Stars_Raw WHERE id >= ? ORDER BY id LIMIT ?', (starID,many))

for star in cur_1 :
    xml=star[1]
    try :
        elem=ET.fromstring(xml)

    except:
        print('Invalid XML for star HD', star[0])
        cur.execute('INSERT OR IGNORE INTO Stars (id, ra, dec, mag, const_id) VALUES (?,NULL,NULL,NULL,NULL)',(star[0],))
        conn.commit()
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

    try :
        cur.execute('INSERT OR IGNORE INTO Stars (id, ra, dec, mag, const_id) VALUES (?,?,?,?,?)',(star[0],rah,dedeg,mag,constid))
        cur.execute('INSERT OR IGNORE INTO Constellations (id, const) VALUES (?,?)', (constid, constname))
        conn.commit()
    except KeyboardInterrupt :
        err=1
        print('Process interrupted by User ...')
        print('Last star cleaned: HD', star[0])
        break

    count=count+1

    if count%1000 == 0: time.sleep(5)
    #print(constid, constname, rah, dedeg, mag)

if err != 1 :
    print('Data cleaning successful')
    print('Last star cleaned: HD', star [0])

cur_1.close()
cur.close()

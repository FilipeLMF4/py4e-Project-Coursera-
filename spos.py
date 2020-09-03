import sqlite3

# Open the main content (Read only)
conn = sqlite3.connect('file:stars.sqlite?mode=ro', uri=True)
cur = conn.cursor()

star=input('Which star to get information? ')

cur.execute('''SELECT Stars.id,ra,dec,mag,const
            FROM Stars JOIN Constellations ON Stars.const_id = Constellations.id
            WHERE Stars.id = ?''', (star,))

row=cur.fetchone()
#print(row)

ra=row[1]
dec=row[2]
mag=row[3]
const=row[4]

#Convert ra to H/M/S
rah=int(ra)
ram=(ra-rah)*60
ras=(ram-int(ram))*60
srah=str(rah)
sram=str(int(ram))
sras=str(round(ras,5))
sra=srah+'h '+sram+'m '+sras+'s'

#Convert dec to º/m/s
decdeg=int(dec)
decmin=abs((dec-decdeg)*60)
decs=(decmin-int(decmin))*60
sdecdeg=str(decdeg)
sdecmin=str(int(decmin))
sdecs=str(round(decs,5))
sdec=sdecdeg+'º '+sdecmin+'\' '+sdecs+'\'\''

print('')
print('Information for Star HD', star)
print('\tDeclination:', sdec)
print('\tRight Ascension:', sra)
print('\tApparent Magnitude:', mag)
print('\tConstellation:', const)

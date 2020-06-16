# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Rolf Lyneborg Lund)s
"""

import win32com.client
outlook = win32com.client.Dispatch("outlook.application")
import pandas as pd
import datetime

df=pd.read_csv(r"C:\Users\Admin\Dropbox\3. AAU\Automation\Booking\AllData2.csv")
df1 = pd.DataFrame(df.Dato.str.split('.',1).tolist(), columns = ['day','Dato'])
df['Dato']=df1['Dato']
df.insert(0, 'id', range(1, 1 + len(df)))
df['Frakl']=(df['Frakl']).astype(str)
df['Tilkl']=(df['Tilkl']).astype(str)

ting='.3'
df['dumting']=df['Frakl'].str.find(ting)
df['dumting']=(df['dumting']).astype(str)
df['dumting'] = df['dumting'].str.replace('-1','')
df['dumting'] = df['dumting'].str.replace('2','0')

df['Frakl']=df['Frakl']+df['dumting']

df['Frakl'] = df['Frakl'].str.replace('.',':')
df['Dato'] = df['Dato'].str.replace('/', ' ')
df['Datofra']=pd.to_datetime(df['Dato'] + ' ' + df['Frakl'], format = ' %d %m %Y %H:%M')
df['Datofra'] +=  pd.offsets.Hour(1)

df['dumting']=df['Tilkl'].str.find(ting)
df['dumting']=(df['dumting']).astype(str)
df['dumting'] = df['dumting'].str.replace('-1','')
df['dumting'] = df['dumting'].str.replace('2','0')

df['Tilkl']=df['Tilkl']+df['dumting']

df['Tilkl'] = df['Tilkl'].str.replace('.',':')

df['Datotil']=pd.to_datetime(df['Dato'] + ' ' + df['Tilkl'])
df['Datotil'] +=  pd.offsets.Hour(1)

df['timediff']=df['Datotil']-df['Datofra']
df['timediff'] = df['timediff'].dt.seconds
df['timediff'] = df['timediff']/60

df['Datofra']=df['Datofra'].dt.strftime('%Y-%d-%m %H:%M')
df['Datotil']=df['Datotil'].dt.strftime('%Y-%d-%m %H:%M')
df['timediff']=(df['timediff']).astype(str)

x="'"
df['Datofra'] = x + df['Datofra'].astype(str) +x
df['timediff'] = df['timediff'].str[:-2]

for index, row in df.iterrows():
    x = df['Datofra'][index]
    x = str(x)
    x = x.replace("\'", "")
    d_x = datetime.datetime.strptime(str(x), '%Y-%d-%m %H:%M')
    d_x = datetime.datetime.strptime(str(x), '%Y-%d-%m %H:%M').strftime('%Y-%m-%d %H:%M')
    d_x = datetime.datetime.strptime(str(d_x), '%Y-%m-%d %H:%M')
    print(df['Beskrivelse'][index])
    print(d_x)
    print(df['timediff'][index])
    print(df['Datofra'])
    # appt = outlook.CreateItem(1)
    # appt.Start = d_x
    # appt.Subject = df['Beskrivelse'][index]
    # appt.Duration = df['timediff'][index]
    # appt.Location = df['Lokale'][index]
    # appt.MeetingStatus = 1
    # appt.Recipients.Add("rolfll@id.aau.dk")
    # appt.Organizer = 'rolfll@id.aau.dk'
    # appt.Save()
    # appt.Send()
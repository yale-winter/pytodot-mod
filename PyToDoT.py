# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 20:08:43 2022

@author: yale-winter
yalewinter.com

- - - - - - - - - - - - - - - - - - - - - - - - -

PyToDoT: Python To-Do Tracker

- - - - - - - - - - - - - - - - - - - - - - - - -

Create a google sheet online or use with .csv offline 
The document needs the following schema:

Collumns: (A)To-Dos  (B)Date Assigned  (C)Date Complete  (D)Priority
Data:        To-do         3.1.22            3.5.22            0
Data:       To-do 2        3.5.22            3.5.22            1
etc ...

To-Do Priority must be greater than 0 to show up when finding next To-Dos

To load your live google sheet online:
Change import_online to True, and replace ___online_url___ with that part of your url

To load your offline .csv:
Download your To-Dos as .csv (only downloading selected collumns and rows)
And name the document 'ToDos.csv' and place in the same folder
Run the script to analyze To-Do productivity and sort for the next To-Dos
See the example .csv file (ToDos.csv) attached in this repository

Run command "to_do(1, df)" in the console to see the full text Description of To-Do ID: 1

"""

import pandas as pd
import os
from datetime import date, timedelta


def to_do(x, df):
    '''
    Print the to-do description from row id
    '''
    print('\nTop To-Do:')
    print('>>>',df.iloc[x][0])

def find_recent_progress(df, prog):  
    '''
    Show information regarding to-do progress in last 30 days
    '''
    days_before = pd.Timestamp((date.today()-timedelta(days=30)))
    df3 = df.iloc[0,1]
    delta = pd.Timestamp(date.today()) - df3
    print('Days since tracking:',delta.days)
    print('Average To-Dos completed in 30 days:', int(prog[0] / delta.days * 30))
    df2 = df.loc[df['Date Complete'] > days_before,]
    print('To-Dos completed in last 30 days:',len(df2))
    
def find_to_do_progress(df):
    '''
    Show information for all to-do progress
    '''
    todos_complete = 0
    todos_in_progress = 0
    for i in range(len(df)):
        if df.iloc[i][2] is pd.NaT:
            todos_in_progress +=1
        else:
            todos_complete += 1  
    print('\nTo-Dos Complete:', todos_complete, '\nTo-Dos In Progress:', todos_in_progress)
    return (todos_complete, todos_in_progress)

def find_next_to_dos(df):
    '''
    Show next to-dos
    '''
    df2 = df.loc[df['Date Complete'].isnull(), ['To-Dos', 'Date Assigned', 'Priority']]
    df3 = df2.loc[df['Priority'] > 0, ['To-Dos', 'Date Assigned', 'Priority']]
    df3 = df3.sort_values(by=['Priority', 'Date Assigned'], ascending = False)
    print(df3)
    to_do(0, df3)

def import_to_dos(file_name, online):
    '''
    Import to-dos from .csv file
    '''
    df = []
    if online:
        df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                           '___online_url___' +
                           '/export?gid=0&format=csv',
                          )
    else:
        # file path (same directory as this file)
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        sheet_url = os.path.join(__location__, file_name)
        df = pd.read_csv(sheet_url, nrows=500, on_bad_lines='skip')
        df.dropna(how='all')
        
    ldf = df.values.tolist()
    #convert datetime
    for i in range(len(ldf)):
        ldf[i][1] = pd.to_datetime(df.iloc[i][1])
        ldf[i][2] = pd.to_datetime(df.iloc[i][2])
    df = pd.DataFrame(ldf, columns=['To-Dos', 'Date Assigned', 'Date Complete', 'Priority'])
    return df

'''
Start up and display To-Do information
'''
import_online = False
df = import_to_dos('ToDos.csv', import_online)
find_next_to_dos(df)
prog = find_to_do_progress(df)
find_recent_progress(df, prog)





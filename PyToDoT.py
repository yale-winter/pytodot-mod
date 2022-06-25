# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 20:08:43 2022

@author: yale-winter
yalewinter.com

- - - - - - - - - - - - - - - - - - - - - - - - -

PyToDoT: Python To-Do Tracker

- - - - - - - - - - - - - - - - - - - - - - - - -

Create a public google sheets (or other .csv) document with the following schema:

Collumns: (A)To-Dos  (B)Date Assigned  (C)Date Complete  (D)Priority
Data:        To-do         3.1.22            3.5.22            0
Data:       To-do 2        3.5.22            3.5.22            1
etc ...

Priority can be in the range of (-1 through 3) -1 being lowest priority, 3 is top priority
Download your To-Dos as .csv (only downloading selected collumns and rows)
And name the document 'ToDos.csv' and place in the same folder
Run the script to analyze To-Do productivity and sort for the next To-Dos'
See the example .csv file (ToDos.csv) attached in this repository
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
    print('Average todos completed in 30 days:', int(prog[0] / delta.days * 30))
    df2 = df.loc[df['Date Complete'] > days_before,]
    print('Todos completed in last 30 days:',len(df2))
    
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
    print('\nTodos Complete:', todos_complete, '\nTodos In Progress:', todos_in_progress)
    return (todos_complete, todos_in_progress)

def find_next_to_dos(df):
    '''
    Show next to-dos
    '''
    df2 = df.loc[df['Date Complete'].isnull(), ['To-Dos', 'Date Assigned', 'Priority']]
    df3 = df2.loc[df['Priority'] >= 1, ['To-Dos', 'Date Assigned', 'Priority']]
    df3 = df3.sort_values(by=['Priority', 'Date Assigned'], ascending = False)
    print(df3)
    to_do(0, df3)

def import_to_dos(file_name):
    '''
    Import to-dos from .csv file
    '''
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
df = import_to_dos('ToDos.csv')
find_next_to_dos(df)
prog = find_to_do_progress(df)
find_recent_progress(df, prog)









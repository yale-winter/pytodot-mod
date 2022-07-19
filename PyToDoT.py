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

To load your offline .csv:
Download your To-Dos as .csv (only downloading selected collumns and rows)
And name the document 'ToDos.csv' and place in the same folder
Run the script to analyze To-Do productivity and sort for the next To-Dos
See the example .csv file (ToDos.csv) attached in this repository

Run command "to_do(1, df)" in the console to see the full text Description of To-Do ID: 1

"""

import pandas as pd
from datetime import date, timedelta
import os


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
    delta = pd.Timestamp(date.today()) - pd.Timestamp(df3)
    print('Days since tracking:',delta.days)
    print('Average To-Dos completed in 30 days:', int(prog[0] / delta.days * 30))
    df2 = df.loc[df['Date Complete'] > str(days_before),]
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
    df = df.loc[df['Date Complete'].isnull(), ['To-Dos', 'Date Assigned', 'Priority']]
    df = df.loc[df['Priority'] > 0, ['To-Dos', 'Date Assigned', 'Priority']]
    df = df.sort_values(by=['Priority', 'Date Assigned'], ascending = False)
    print(df)
    to_do(0, df)
    
def fix_dates_in_col(df, col_index, col_names):
    '''
    Formats dates in a collumn
    ----------
    Returns
    -------
    modified DataFrame

    '''

    ldf = df.values.tolist()
    for i in range(1, len(ldf)):
        try:
            r = pd.to_datetime(df.iloc[i][col_index], errors='coerce')
            r = r[:10]
            ldf[i][col_index] = r
        except:
            pass
    df = pd.DataFrame(ldf, columns=col_names)  

    return df

def import_data_table(file_name, read_rows, col_names):
    '''
    Import timeline from .csv file
    
    Parameters
    ----------
    file_name : string
        File name including file extension
    online : bool
        Read online or local
    read_rows : number
        number of rows to read
    col_names : array of strings
        names of columns

    Returns
    -------
    DataFrame of the content or error string

    '''
    df = 'error importing data'
    try:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        sheet_url = os.path.join(__location__, file_name)  
        df = pd.read_csv(sheet_url,nrows=read_rows, on_bad_lines='skip')
        print('loaded data table from local .csv')
    except:
        print('error loading data from local .csv')
    
    # drop rows where at least 1 element is missing
    if type(df) == pd.DataFrame:
        df.dropna()
    return df

def start():
    '''
    Start up and display To-Do information
    '''
    col_names = ['To-Dos', 'Date Assigned', 'Date Complete', 'Priority']
    df = import_data_table('ToDos.csv', 1000, col_names)
    df = fix_dates_in_col(df, 1, col_names)
    df = fix_dates_in_col(df, 2, col_names)
    find_next_to_dos(df)
    prog = find_to_do_progress(df)
    find_recent_progress(df, prog)

    return df
    
df = start()





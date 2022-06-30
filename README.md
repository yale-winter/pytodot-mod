- - - - - - - - - - - - - - - - - - - - - - - - -
**PyToDoT: Python To-Do Tracker**
- - - - - - - - - - - - - - - - - - - - - - - - -
Create a google sheet online or use with .csv offline with the following schema:

| To-Dos | Date Assigned | Date Complete | Priority |
| --- | --- | --- | --- |
| To-do | 3.1.22 | 3.5.22 | 0 |
| To-do 2 | 3.5.22 | 3.5.22 | 1 |


**To load your live google sheet online:**<br/>
Change import_online to True, and replace ___online_url___ with that part of your url<br/><br/>
**To load your offline .csv:**<br/>
Download your To-Dos as .csv (only downloading selected collumns and rows)<br/>
And name the document 'ToDos.csv' and place in the same folder<br/><br/>
**How to Use:**
- Run the script to analyze To-Do productivity and sort for the next To-Dos
- See the example .csv file (ToDos.csv) attached in this repository
- To-Do Priority must be greater than 0 to show up when finding next To-Dos
- Run command "to_do(1, df)" in the console to see the full text Description of To-Do ID: 1

![PyToDoT](https://user-images.githubusercontent.com/5803874/175763591-e8261c2d-d28c-4527-a3d6-aa3672ad4171.jpg)

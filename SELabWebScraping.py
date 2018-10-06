#improvements:
#get actual section number
#make sure script can get any page

from bs4 import BeautifulSoup
import re
import requests
import tkinter
from tkinter import messagebox

#fixes duplicate table row closes
def cleanup(htmlString):
    pattern = re.compile('</tr>\s*</tr>')
    return re.sub(pattern, '</tr>', htmlString)

#returns the number of seats available in the class from its tr tag
def extract_seats(tag):
    s = tag.find_all('td')[14].text.strip().lower()
    if s == 'full':
        return 0
    else:
        return int(s)

#returns true if a tag is a tr with class 'odd' or 'even'
def is_data_row(tag):
    return tag.name == 'tr' and tag.has_attr('class') and (tag['class'][0] == 'odd' or tag['class'][0] == 'even')

#get the website
print('Getting class schedule... ', end = '')
website = requests.get('http://classschedule.wayne.edu/sections_new.cfm?subj=CSC&course=4111&campus=NOSELECTION&instr=NOSELECTION')
print('done')
text = cleanup(website.text)

#validate that the fall term is selected

if 'Fall Term 2018' in text:
    print('Fall Term 2018 found')
else:
    print('WARNING: Fall Term 2018 NOT found')

#parse the html and find the table
soup = BeautifulSoup(text, "html.parser")
soup = soup.find('table', id = 'maintable')

#get the data rows
rows = soup.find_all(is_data_row)
print(len(rows), 'rows found')

#extract row data
data = []
for row in rows:
    data.append(extract_seats(row))

#generate message box message
message_lines = []
for i in range(len(data)):
    if data[i] == 0:
        message_lines.append('Section ' + str(i + 1) + ' is full')
    else:
        message_lines.append('Section ' + str(i + 1) + ' has ' + str(data[i]) + ' seat(s) open!!!')
message = '\n'.join(message_lines)

#display message box
root = tkinter.Tk()
root.withdraw() #hide main window
messagebox.showinfo('Class Schedule Info', message)

#cleanup
website.close()

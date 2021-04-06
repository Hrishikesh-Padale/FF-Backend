import requests
from bs4 import BeautifulSoup
import csv

url = "https://in.finance.yahoo.com/screener/predefined/most_actives/?count=25&offset=0"
r = requests.get(url)
htmlcontent = r.content
#find count of data
soup = BeautifulSoup(htmlcontent, 'html.parser')
dc = soup.find('span', class_="Mstart(15px)")
totcount = int(str(dc.text).split()[2])
tot_surf = totcount//25 +1
#table titles
div  =  soup.find('table')
thead = div.find('thead')
tit = []
for row in thead.find_all('th', class_="Ta(start)"):
    tit.append(row.text)
for cols in thead.find_all('th', class_="Ta(end)"):
    tit.append(cols.text)
del tit[0]
#parsing each page until data recovered
table = []
for i in range(tot_surf):
    url = "https://in.finance.yahoo.com/screener/predefined/most_actives/?count=25&offset="+str(i*25)
    r = requests.get(url)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    div  =  soup.find('table')
    for tab in div.find_all('tbody'):
        rows = tab.find_all('tr')
        for row in rows:
            ro = []
            for col in row.find_all('td'):
                ro.append(col.text)
            del ro[0]
            table.append(ro)
table.insert(0, tit)

table = table[1:]
with open('data.csv','w+',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table)
          
#print(tit)
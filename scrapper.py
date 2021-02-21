from bs4 import BeautifulSoup
import requests
import time
import csv

soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_brown_dwarfs").text, "html.parser")
rows = soup.find_all("table", attrs={"class", "wikitable"})[0].find_all('tr')
rows.pop(0)

headers = ['Star', 'Constellation', 'Rightascension', 'Declination', 'App.mag.', 'Distance', 'Spectraltype', 'Brown dwarf', 'Mass', 'Radius', 'Orbitalperiod', 'Semimajoraxis', 'Ecc.', 'Discovery year', 'Link']
data = []

for row in rows:
    temp = []
    link = ''
    
    for index, td in enumerate(row.find_all('td')):
        temp.append(td.text.strip())

        if index == 0:
            link = 'https://en.wikipedia.org' + td.find('a')['href']
            
    temp.append(link)
    data.append(temp)


for index, i in enumerate(data):
    soup = BeautifulSoup(requests.get(i[-1]).text, "html.parser")

    try:
        rows = soup.find_all("table", attrs={"class", "wikitable"})[0].find_all('tr')

        for row in rows:
            for td in row.find_all('td'):
                td = (td.text.strip())

                if td == '—':
                    data[index].append("")
                
                else:
                    data[index].append(td)
                
    except:
        pass
 
with open("data.csv", "w", newline='', encoding='utf-8') as f:
  writer = csv.writer(f)
  writer.writerow(headers)
  writer.writerows(data)


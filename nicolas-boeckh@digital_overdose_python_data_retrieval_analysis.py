# pip install requests bs4 lxml pandas

####################  PART 1: Requests  ####################

import requests
from codecs import open as copen

r = requests.get('https://web.archive.org/web/20160424191931/http://www.disastercenter.com/crime/Florida%20crime%20and%20punishment%20statistics.html')

print(r.status_code)
print(r.content[0:100])

f = copen('data.html', 'w', encoding='utf-8')
f.write(r.content.decode('utf-8'))
f.close()

####################  PART 2: BS4  ####################

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content.decode("utf-8"))

tables = []
for node in soup.findAll("table"):
	tables += [node]
	
table = tables[4]
data = []

for row in table.findAll('tr'):
    col = row.findAll('td')
	data += [(col[0].getText(), col[1].getText(), col[2].getText(), col[3].getText())]
	
data[1:]
data2 = []
for d in data:
	if data[0] != ' Year ':
		data2 += [d]
	
data3 = []	
for d in data2:
	data3 += [(int(d[0]), float(d[1]), float(d[2]), float(d[3]))]	

####################  PART 3: pandas  ####################

import pandas as pd
dfs = pd.read_html('data.html', encoding='utf-8')

df = dfs[5]

print(df.columns) # -> Returns int's because no headers were set
df = df.rename(columns={0: 'Year', 1: 'Inmates per 100k', 2: 'New Index *', 3: 'Index per Inmates'})
df = df[df.index > 0]
df = df[df.Year != "Year"]

print(df['Year'])
print(list(df['Year']))

print(list(map(lambda x: int(x), df['Year'])))

print(df[df.Year >= '2000'])
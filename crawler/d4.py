from bs4 import BeautifulSoup
import urllib.request
import requests
import csv
import pandas as pd
import time

df1 = pd.read_csv('restaurant.csv')
df2 = pd.read_csv('cafe.csv')
df3 = pd.read_csv('hotel.csv')
df4 = pd.read_csv('night life.csv')
df_list = [df1, df2, df3, df4]
keywords = ['restaurant0','cafe0','hotel0','night life0']


description_list = []
count = 0
for name in df4['Name']:
    if count % 15 == 0:
        time.sleep(60)
    query = name
    query = query.replace(' ', '+')
    url = 'https://www.google.com/search?q=' + query + '&lr=lang_en&cr=countryUS'

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}
    page = requests.get(url, headers = headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        
        span = soup.find_all('span', {'class': 'Yy0acb'})
        if len(span) != 0:
            s = str(span[0])
            result = s[21:len(s)-7]
            description_list.append(result)
            print('found one!')
        else:
            description_list.append('')
            print('not found!')
    else:
        description_list.append('')
        print('status_code!')
    count += 1

    
df4['Description'] = description_list
df4.to_csv(keywords[3] + '.csv')
print('saved csv!')
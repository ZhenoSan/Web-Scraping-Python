'''
    Code For Data Extraction and Wrangling
    
    References:
    
    https://github.com/CoderVloggerArchive/web-scraping-python-wikipedia
    https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html

'''

import bs4
import requests
import re
import pandas as pd

response = requests.get("https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals").text

mainlist = []
if response is not None:
    soup = bs4.BeautifulSoup(response,'lxml') #'html.parser')
    for items in soup.find('table', class_='sortable plainrowheaders wikitable').find_all('tr')[1:-4]:
        data = items.find_all(['th','td'])
        try:
            A = '2002' if (data[5].a.text=='Yokohama') else data[0].span.find_next_sibling().text
            #Year.append(data[0].a.text)
            B = data[5].a.text
            C = data[5].a.find_next_sibling().text
            #Hosts.append(data[1].a.text)
            D = data[1].a.text
            E = data[2].a.text
            F = data[3].a.text
        except IndexError:pass
        except AttributeError:pass
        print(f"{A}|{B}|{C}|{D}|{E}|{F}")
        mainlist.append([A,B,C,D,E,F])
        
df = pd.DataFrame.from_records(mainlist)
df.columns = ['Year','Venue','Host','Winner','Score','Runner-Up']#,'Runner-Up_Score']
df['Winner_Score'] = df.Score.str.split('–').str[0].astype('int32')
df['Runner_Up_Score'] = df.Score.str.split('–').str[1].astype('int32')
df.drop(columns='Score',inplace=True)
df.drop_duplicates('Year',inplace = True)
df.replace('West Germany','Germany',inplace=True)
df.to_csv('FIFA_WorldCup_Results.csv', index=False,encoding='utf_8_sig')

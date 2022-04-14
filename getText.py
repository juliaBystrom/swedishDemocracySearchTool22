import pandas as pd
from bs4 import BeautifulSoup

def getDf(file):
    df = pd.read_csv(file, names=['x1', 'id', 'year', 'x2', 'type', 'x3', 'x4', 'part', 'x5', 'x6', 'x7', 'date1', 'date2', 'name', 'x8', 'fetched', 'ref'])
    df = df.drop(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'name', 'ref'], axis=1)
    return df

df_90_99 = getDf("sou-1990-1999.csv")
df_00_04 = getDf("sou-2000-2004.csv")
df_05_09 = getDf("sou-2005-2009.csv")
df_10_14 = getDf("sou-2010-2014.csv")
df_15_ = getDf("sou-2015-.csv")

for id in df_90_99[['id']].to_numpy():
    url = "https://data.riksdagen.se/dokumentstatus/" + str(id[0]) 
    response = requests.get(url)
    soup1 = BeautifulSoup(response.text, 'lxml')
    dokument = soup1.dokumentstatus.dokument
    titel = dokument.titel.text         # sou rm nummer
    rm = dokument.rm.text               # year
    nummer = dokument.nummer.text   
    relaterat_id = dokument.relaterat_id.text
    subtitel = dokument.subtitel.text
    soup2 = BeautifulSoup(dokument.get_text(), 'html.parser')
    text = soup2.get_text()
    break

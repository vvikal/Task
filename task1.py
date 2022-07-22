
import numpy as np
import pandas as pd
import time
start_time = time.time()

#getting data from google sheet as dataframe.
sheet_id = "1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM"
sheet_name = "Sheet1"
url = "https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/edit#gid=0"
url_1 = url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1).head(100)
df.head(4)

df.info()

from bs4 import BeautifulSoup
import requests
import json
import sqlite3

#getting html from url funtion
def getHTMLdocument(url):
    response = requests.get(url)
    return response.text

#creating connection to save in database
conn = sqlite3.connect('test.db')
print("Opened database successfully")

#creating table in database
conn.execute('''CREATE TABLE IF NOT EXISTS WEB_INFO
        (Title              TEXT ,
        Image_URL           TEXT,
        Product_Price       TEXT,
        Product_Details     TEXT );''')
print("Table created successfully")

  
data_list = []
final_list = []

#iterating through list to get country and Asin.
for country,asin in zip(df.country, df.Asin):
  url_to_scrape = "https://www.amazon."+country+"/dp/"+asin
  r = requests.get("http://httpbin.org/redirect/1")

  #checking if url works
  if r.status_code == 404:
    print(url_to_scrape)

  #performing action to get required input.
  else:
    html_document = getHTMLdocument(url_to_scrape)  
    soup = BeautifulSoup(html_document, 'html.parser')
    print("Title:{} :: Image URL:{} :: Price:{} :: Product Details:{}".format(soup.title.text.replace('\n',''),images['src'],price,product))
    images = soup.find('img')
    price = soup.find('price')
    product = soup.find('Product')
    title_list = ["Title","Image URL", "Product Price","Product Details"]
    data_list = [soup.title.text,images['src'],soup.price,soup.product]
    conn.execute("INSERT INTO WEB_INFO (Title,Image_URL,Product_Price,Product_Details) VALUES ('"+soup.title.text+"', '"+images['src']+"', '"+str(soup.price)+"', '"+str(soup.product)+"');")
    random_dict = dict(zip(title_list, data_list))
    final_list.append(random_dict)

#converting list in json 
final_json = json.dumps(final_list, indent=4)

#commiting changes in database.
conn.commit()
print("Records created successfully")
conn.close()
end_time = time.time()

Total_time = start_time-end_time
print("Total Time taken :" )
print(Total_time)


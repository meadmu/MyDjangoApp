import requests
from bs4 import BeautifulSoup
from .models import StockMarket
from django.db import connection


class WebRequest():

    def getRequest(insert,clean,update):

        
        try:
            URL = "https://www.nadirdoviz.com/mobil/fiyatekrani.aspx?grupid=99"
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            results = soup.find(id="stockTable")
            # print(results.prettify())


            stock_elements = results.find_all("tr", class_="trfiyat")

            for stock_element in stock_elements:
                title = stock_element.find("td", class_="fadsl")
                value = stock_element.find("td", class_="fadg")
                
                try:  
                    val_flo=float(value.text.replace('.','').replace(',','.'))
                    #Stock.objects.create(name=title.text,value=val_flo)
                    cursor = connection.cursor()
                    dataset = (title.text,val_flo)
                    if (insert==1):
                        cursor.execute(f"INSERT INTO myapp_stockmarket(name,value) VALUES ('{dataset[0]}',{dataset[1]});")
                    if (update==1):
                        cursor.execute(f"UPDATE myapp_stockmarket set value='{dataset[1]}' where name='{dataset[0]}'")
                except:
                    pass
        except:
            pass

        if (clean==1):

            rows=StockMarket.objects.all()
            for row in rows:
                row.delete()









        
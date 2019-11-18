import requests
from bs4 import BeautifulSoup as soup

from database_holder import session,Stock

symbol = "ZEEL"
url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol={}&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=week".format(symbol)
response = requests.get(url)

response_str = response.content.decode("utf-8").strip()
html = soup(response_str,"html.parser")
table = html.find("table")
if table is not None:
    data_row = table.findAll("tr")[-1]
    headers = ["Date","Symbol","Series","Open Price","High Price","Low Price","Last Traded Price","Close Price","Total Traded Quantity","Turnover (in Lakhs)"]
    actual_data = []
    for cell in data_row.findAll("td"):
        actual_data.append(cell.string.strip())
    date,symbol,series,open_price,high_price,low_price,last_traded_price,close_price,total_traded_quantity,turnover = actual_data
    a_stock = Stock(symbol=symbol, date=date, today_open=open_price, today_close=close_price,
                    traded_quantity=total_traded_quantity)
    session.add(a_stock)
    session.commit()

    stocks = session.query(Stock).all()
    print(stocks)
else:
    print("Couldn't find the content")
    print("Maybe yesterday is Sunday or Market holiday")


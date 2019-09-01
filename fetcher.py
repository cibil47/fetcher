import requests
from bs4 import BeautifulSoup as soup
import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://admin:admin@127.0.0.1:3306/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Stock(Base):

  __tablename__ = 'stocks'
  id = Column(Integer, primary_key=True)
  symbol = Column(String(10))
  date = Column(String(15))
  lastPrice = Column(String(10))
  previousClose = Column(String(10))
  today_open = Column(String(10))
  today_close = Column(String(10))
  today_min = Column(String(10))
  today_max = Column(String(10))

  def __repr__(self):
    return f"<Stock(symbol={self.symbol}, lastUpdateTime={self.date}, lastPrice={self.lastPrice})>"


Base.metadata.create_all(engine)

symbol = "ZEEL"
url = f"https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={symbol}&illiquid=0&smeFlag=0&itpFlag=0"
# url2 = f"https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol={symbol}&series=EQ"

get_header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
              "Accept-Encoding":"gzip, deflate, br",
              "Cache-Control": "max-age=0",
              "Host": "www.nseindia.com",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
              "Sec-Fetch-Mode": "navigate",
              "Sec-Fetch-Site": "none",
              "Sec-Fetch-User": "?1",
              "Upgrade-Insecure-Requests": "1"}

data = requests.get(url,headers = get_header)
response =  data.content
html_parser = soup(response,"html.parser")

div_html = html_parser.find("div", {"id": "responseDiv"})
div_data = div_html.contents[0].strip()
div_json = json.loads(div_data)

symbol = div_json["data"][0]["symbol"]
date = div_json["tradedDate"]
lastPrice = div_json["data"][0]["lastPrice"]
previousClose = div_json["data"][0]["previousClose"]
day_open = div_json["data"][0]["open"]
day_close = div_json["data"][0]["closePrice"]
day_high = div_json["data"][0]["dayHigh"]
day_low = div_json["data"][0]["dayLow"]

a_stock = Stock(symbol=symbol, date=date, lastPrice=lastPrice,previousClose=previousClose,today_open=day_open,today_close=day_close,today_min=day_low,today_max=day_high)
session.add(a_stock)
session.commit()
# stocks = session.query(Stock).all()
# print(stocks)
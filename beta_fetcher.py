import requests
import json
from bs4 import BeautifulSoup as soup  # HTML parser
# ORM imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///stocks.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Stock(Base):

  __tablename__ = 'stocks'
  id = Column(Integer, primary_key=True)
  symbol = Column(String)
  lastUpdateTime = Column(String)
  lastPrice = Column(String)
  previousClose = Column(String)
  today_open = Column(String)
  today_close = Column(String)
  today_min = Column(String)
  today_max = Column(String)

  def __repr__(self):
    return f"<Stock(symbol={self.symbol}, lastUpdateTime={self.lastUpdateTime}, lastPrice={self.lastPrice})>"


# Base.metadata.create_all(engine)
for i in ["YESBANK","JSWSTEEL"]:
  symbol_to_search = i
  url = f"https://beta.nseindia.com/api/quote-equity?symbol={symbol_to_search}"
  data = requests.get(url)
  response_data = data.content
  response_json = json.loads(response_data)
  print(response_json)

  symbol = response_json["metadata"]["symbol"]
  lastUpdateTime = response_json["metadata"]["lastUpdateTime"]
  lastPrice = response_json["priceInfo"]["lastPrice"]
  previousClose = response_json["priceInfo"]["previousClose"]
  today_open = response_json["priceInfo"]["open"]
  today_close = response_json["priceInfo"]["close"]
  today_min = response_json["priceInfo"]["intraDayHighLow"]["min"]
  today_max = response_json["priceInfo"]["intraDayHighLow"]["max"]

  print(symbol)
  # print(lastUpdateTime)
  # print(lastPrice)
  # print(previousClose)
  # print(today_open)
  # print(today_close)
  # print(today_min)
  # print(today_max)


  a_stock = Stock(symbol=symbol, lastUpdateTime=lastUpdateTime, lastPrice=lastPrice,previousClose=previousClose,today_open=today_open,today_close=today_close,today_min=today_min,today_max=today_max)
  session.add(a_stock)
session.commit()
stocks = session.query(Stock).all()
print(stocks)
quit()
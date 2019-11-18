from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///stocks.sqlite")
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
  today_open = Column(String(10))
  today_close = Column(String(10))
  traded_quantity = Column(String(10))

  def __repr__(self):
    return "Stock(symbol={}, lastUpdateTime={}, lastPrice={})".format(self.symbol,self.date,self.today_close)

Base.metadata.create_all(engine)
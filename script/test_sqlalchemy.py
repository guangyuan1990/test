from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import pymysql.cursors



Base = declarative_base()

class tester(Base):
    __tablename__ = 'tester'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    iphone = Column(String(64))
    


engine = create_engine('mysql+pymysql://root@111.230.238.124:3306/mysql', echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base.metadata.create_all(engine)

test = tester(name='yhgtest12',iphone='12345')
session.add(test)
session.commit()

#my_db = session.query(plugin).all()
#print(my_db)

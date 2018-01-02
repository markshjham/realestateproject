from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    rentOrSale = Column(Integer, nullable=False)
    bedroom = Column(Integer, nullable=False)
    bathroom = Column(Integer, nullable=False)
    sqft = Column(Integer)
    lat = Column(Integer, nullable=False)
    lng = Column(Integer, nullable=False)

engine = create_engine('sqlite:///propertylisting.db')

Base.metadata.create_all(engine)

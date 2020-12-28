import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



### begin ###

Base = declarative_base()

### class ###


class Restaurant(Base):
	### table ###
	__tablename__ = 'restaurant'
	
	### mapper ###
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)


class MenuItem(Base):
	### table ###
	__tablename__ = 'menu_item'

	### mapper ###
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)


### end statements ####

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
# Database initial SETUP

# Configuration ORM sqlalchemy - beginning of file
# imports all modules needed
# creates instances of declarative base
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Creates Classes and Tablename and Mappers
class Restaurant(Base):

        # Tablename
        __tablename__ = 'restaurant'

        # Mapper
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)

class MenuItem(Base):

        # Tablename
        __tablename__ = 'menu_item'

        # Mapper
        id = Column(Integer, primary_key=True)
        name = Column(String(80), nullable=False)
        description = Column(String(250))
        price = Column(String(8))
        course = Column(String(250))
        restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
        restaurant = relationship(Restaurant)


# Configuration - End of file
# Creates (or connect) the database and add tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

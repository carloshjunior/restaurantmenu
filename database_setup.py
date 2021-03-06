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

        # We added this serialize function to be able to send JSON objects in a
        # serializable format
        @property
        def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
            }



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

        # We added this serialize function to be able to send JSON objects in a
        # serializable format
        @property
        def serialize(self):
            return {
                'name': self.name,
                'description': self.description,
                'id': self.id,
                'price': self.price,
                'course': self.course,
            }

# Configuration - End of file
# Creates (or connect) the database and add tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

#!/usr/bin/python3
""" Storage for DBStorage to create new engine """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv

Base = declarative_base()


class DBStorage:
    """Database storage engine using SQLALchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization method"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".format
                                      (user, pwd, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        Bse.metadata.create_all(self.__engine)

    def all(self, cls=None):
        """Queries objects depending on the class name"""
        obj_dict = {}
        classes = [cls] if cls else [State, City]

        for c in classes:
            objs = self.__session.query(c).all()
            for obj in objs:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all tbles in the database and creates a new session"""
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """ closes the current database session"""
        self.__session.close()

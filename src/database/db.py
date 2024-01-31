import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.conf.config import settings

URI = settings.sqlalchemy_database_url

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """
    The get_db function is a context manager that will automatically close the database session when it goes out of scope.
    It also handles any exceptions that occur within the with block, converting them into an appropriate HTTP response.
    
    :return: A context manager
    :doc-author: Trelent
    """
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()

from datetime import date, timedelta, datetime
from typing import List

from fastapi import Depends, HTTPException, Path, status, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=10))])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
        The limit and offset parameters are used to paginate the results.
        
    
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of results returned
    :param offset: int: Specify the number of records to skip before returning the results
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        Args:
            contact_id (int): The id of the contact to return.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_email/{email}", response_model=ContactResponse)
async def get_contact_by_email(email: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_email function returns a contact by email.
        Args:
            email (str): The email of the contact to be returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth service. Defaults to Depends(auth_service.get_current_user).
    
    :param email: str: Get the email of the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_phone/{phone}", response_model=ContactResponse)
async def get_contact_by_phone(phone: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_phone function returns a contact by phone number.
        Args:
            phone (str): The phone number of the contact to be returned.
            db (Session, optional): SQLAlchemy Session instance. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
        Returns:
            Contact: A single Contact object matching the provided criteria or None if no match is found.
    
    :param phone: str: Get the phone number of a contact
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is making the request
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_phone(phone, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_first_name/{first_name}", response_model=ContactResponse)
async def get_contact_by_first_name(first_name: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_first_name function returns a contact by first name.
        Args:
            first_name (str): The first name of the contact to be returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object containing user information from the JWT token payload. 
                Defaults to Depends(auth_service.get_current_user).
    
    :param first_name: str: Pass the first name of the contact to be retrieved
    :param db: Session: Get the database session from the dependency injection
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_first_name(first_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_second_name/{second_name}", response_model=ContactResponse)
async def get_contact_by_second_name(second_name: str, db: Session = Depends(get_db),
                                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_second_name function returns a contact by second name.
    
    :param second_name: str: Pass in the second name of the contact that you want to retrieve
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_second_name(second_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_birth_date/{birth_date}", response_model=ContactResponse)
async def get_contact_by_birth_date(birth_date: date, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_birth_date function returns a contact by birth date.
        
    
    :param birth_date: date: Get the date from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is currently logged in
    :return: A contact object, which is defined in models
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_birth_date(birth_date, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, and returns the newly created contact.
    
    :param body: ContactModel: Define the request body
    :param db: Session: Get a database session
    :param current_user: User: Get the user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and db as parameters.
        It returns a ContactModel object if successful.
    
    :param body: ContactModel: Pass the data to be updated
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id of the current user
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The user currently logged in and making this request. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthday_list/", response_model=list[ContactResponse])
async def get_birthday_list(db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_birthday_list function returns a list of contacts with birthdays in the next 7 days.
        The function takes two parameters: start_date and end_date.
        The start date is today's date, and the end date is today's date plus 7 days.
    
    :param db: Session: Get the database connection
    :param current_user: User: Get the user id from the token
    :return: A list of contacts
    :doc-author: Trelent
    """
    start_date = datetime.now().date()
    delta = 7
    end_date = start_date + timedelta(days=delta)
    contacts = await repository_contacts.get_contacts_birthday(start_date, end_date, current_user, db)
    return contacts

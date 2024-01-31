from datetime import date
from src.database.models import Contact, User
from src.schemas import ContactModel
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Determine how many contacts to skip before returning the results
    :param user: User: Get the user_id from the database
    :param db: Session: Pass in a database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on the id of that contact.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User who owns this Contact.
            db (Session): A connection to our database, used for querying and updating data in our tables.
    
    :param contact_id: int: Get the contact by id
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_email(email: str, user: User, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            email (str): The email address of the contact to be retrieved.
            user (User): The user who owns this contact.
            db (Session): A database session for querying and updating data in the database.
    
    :param email: str: Pass in the email address of the contact we want to get from our database
    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact object from the database
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_phone(phone: str, user: User, db: Session):
    """
    The get_contact_by_phone function returns a contact object from the database based on the phone number and user id.
        Args:
            phone (str): The phone number of the contact to be retrieved.
            user (User): The User object that is associated with this contact.
            db (Session): A session for interacting with our database.
        Returns: 
            Contact: A Contact object containing information about a specific person in your contacts list.
    
    :param phone: str: Get the phone number of a contact
    :param user: User: Get the user_id from the logged in user
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.phone == phone, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_first_name(first_name: str, user: User, db: Session):
    """
    The get_contact_by_first_name function returns a contact object from the database based on the first name of that contact.
        Args:
            first_name (str): The first name of the desired contact.
            user (User): The user who owns this particular contact.
            db (Session): A session to connect to our database with.
        Returns: 
            Contact: A single Contact object from our database, or None if no such Contact exists.
    
    :param first_name: str: Filter the database by first name
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass in the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_second_name(second_name: str, user: User, db: Session):
    """
    The get_contact_by_second_name function returns a contact object from the database based on the second_name parameter.
        
    
    :param second_name: str: Filter the database query
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact with the second name that you have specified
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.second_name == second_name, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_birth_date(birth_date: date, user: User, db: Session):
    """
    The get_contact_by_birth_date function returns a contact object from the database based on the birth_date and user.
        Args:
            birth_date (str): The date of birth for which to search.
            user (User): The User object that owns this contact.
            db (Session): A SQLAlchemy Session instance used to query the database.
    
    :param birth_date: date: Specify the birth date of the contact
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.birth_date == birth_date, Contact.user_id == user.id)).first()
    return contact


async def create(body: ContactModel, current_user: User, db: Session):
    """
    The create function creates a new contact in the database.
        
    
    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the current user who is logged in
    :param db: Session: Access the database
    :return: A contact object, but the response is a dict
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user=current_user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user. 
                This is a JSON object containing first_name, second_name, email, phone and birth_date fields.
            user (User): A User object representing the current logged-in user making this request.
                This is used to ensure that only contacts belonging to this specific user are updated by themselfs or an admin/superuser account with access rights over their data.&quot;
    
    :param contact_id: int: Identify the contact to update
    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: The contact object, but the response is empty
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birth_date = body.birth_date
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
        
    
    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_birthday(start_date: date, end_date: date, db: Session):
    """
    The get_contacts_birthday function returns a list of contacts whose birthdays fall between the start_date and end_date.
    The function takes in three parameters:
        - start_date: The first date to search for birthdays (inclusive)
        - end_date: The last date to search for birthdays (inclusive)
        - db: A database session object that is used to query the database. This parameter is required by FastAPI, but not used in this function.
    
    :param start_date: date: Set the start date of the range
    :param end_date: date: Determine the end date of the range
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that have their birthday between the start and end date
    :doc-author: Trelent
    """
    birth_day = extract('day', Contact.birth_date)
    birth_month = extract('month', Contact.birth_date)
    contacts = db.query(Contact).filter(
        birth_month == extract('month', start_date),
        birth_day.between(extract('day', start_date), extract('day', end_date))
    ).all()
    return contacts

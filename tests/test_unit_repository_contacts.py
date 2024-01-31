import unittest
from unittest.mock import MagicMock
from datetime import date
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    get_contact_by_phone,
    get_contact_by_first_name,
    get_contact_by_second_name,
    get_contact_by_birth_date,
    create,
    update,
    remove,
    get_contacts_birthday
)

class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):       
        self.user = User(id=1, username='test_user', password='qwerty', email='test@gmail.com')
        self.session = MagicMock(spec=Session)

    async def test_get_contacts(self):        
        contacts = [Contact(), Contact(), Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.all.return_value = contacts
        self.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = mocked_contacts
        limit = 10
        offset = 0
        result = await get_contacts(limit, offset, self.user,self.session)
        self.assertEqual(result, contacts)
    
    async def test_get_contacts_by_id(self):  
        contacts_id = 1      
        contact = Contact(id=contacts_id, user_id=self.user.id)
        
        self.session.query.return_value.filter.return_value.first.return_value = contact
        result = await get_contact_by_id(contacts_id, self.user, self.session)
        self.assertEqual(result, contact)
    
    async def test_get_contact_by_email(self):        
        email = "test@gmail.com"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_email(email, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)
    
    async def test_get_contact_by_phone(self):        
        phone = "0996458877"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_email(phone, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)
    
    async def test_get_contact_by_phone(self):        
        phone = "0996458877"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_phone(phone, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)
    
    async def test_get_contact_by_first_name(self):        
        first_name = "Sam"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_first_name(first_name, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)

    async def test_get_contact_by_second_name(self):        
        second_name = "Test"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_second_name(second_name, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)
    
    async def test_get_contact_by_birthday(self):        
        birthday = "2000-07-14"
        mocked_contact = MagicMock()
        db_session = MagicMock()        
        db_session.query().filter().first.return_value = MagicMock()
        result = await get_contact_by_birth_date(birth_date=birthday, user=mocked_contact, db=db_session)
        self.assertIsNotNone(result)
    
    async def test_create(self): 
        #create(body: ContactModel, current_user: User, db: Session):       
        body = MagicMock()
        current_user = MagicMock()
        db_session = MagicMock()       
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None       
        result = await create(body, current_user, db_session)        
        self.assertIsNotNone(result)

    async def test_update(self): 
        #update(contact_id: int, body: ContactModel, user: User, db: Session):
        contact_id = 1
        body = MagicMock()
        current_user = MagicMock()
        db_session = MagicMock()       
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None       
        result = await update(contact_id, body, current_user, db_session)        
        self.assertIsNotNone(result)
    
    async def test_remove(self): 
        #remove(contact_id: int, user: User, db: Session):
        contact_id = 1        
        current_user = MagicMock()
        db_session = MagicMock()       
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None       
        result = await remove(contact_id,  current_user, db_session)        
        self.assertIsNotNone(result)
    
    async def test_get_contacts_birthday(self): 
        #get_contacts_birthday(start_date: date, end_date: date, db: Session):
        start_date = date(2024, 1, 28)
        end_date = date(2024, 2, 14)
        db = MagicMock() 
        contacts_range = [MagicMock(), MagicMock(), MagicMock()]       
        db.query().filter().all.return_value = contacts_range     
        result = await get_contacts_birthday(start_date, end_date, db)        
        self.assertEqual(len(result), len(contacts_range))
   

if __name__ == '__main__':
    unittest.main()
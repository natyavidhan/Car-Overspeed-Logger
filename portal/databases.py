from pymongo import MongoClient
import uuid
from datetime import datetime
import re
import os
import bcrypt


class Database:
    def __init__(self):
        connection = MongoClient(os.environ['MONGO_URI'])['COL']
        self.users = connection['users']
        self.reports = connection['reports']
        self.locations = connection['locations']
        self.admin = connection['admin']
        self.portal_reports = connection['portal_reports']
        
    def userExist(self, email=None, ID=None):
        if email is not None:
            return self.users.find_one({'email': email}) is not None
        elif ID is not None:
            return self.users.find_one({'_id': ID}) is not None
        else:
            return False
    
    def getUser(self, email=None, ID=None):
        if email is not None:
            return self.users.find_one({'email': email})
        elif ID is not None:
            return self.users.find_one({'_id': ID})
        else:
            return None
    
    def registerUser(self, email, password, name, role='user'):
        if self.userExist(email=email):
            return False
        elif re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email) is None:
            return False
        else:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.users.insert_one({
                '_id': str(uuid.uuid4()),
                'email': email,
                'password': password,
                'name': name,
                'role': role,
                'created': datetime.now()
            })
            return True
    
    def authenticate(self, email, password):
        user = self.getUser(email=email)
        if user is None:
            return False
        else:
            return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
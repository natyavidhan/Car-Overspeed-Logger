from pymongo import MongoClient
import uuid
from datetime import datetime
import re
import os


class Database:
    def __init__(self):
        connection = MongoClient(os.environ['MONGO_URI'])['COL']
        self.users = connection['users']
        self.reports = connection['reports']
        self.locations = connection['locations']
        self.admin = connection['admin']
        self.portal_reports = connection['portal_reports']
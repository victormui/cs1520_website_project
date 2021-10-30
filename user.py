import datetime
import flask
from google.cloud import datastore
from flask import request

def get_client():
    return datastore.Client()

class User():
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def get_username(self):
        return '%s' % (self.username)
    def get_password(self):
        return '%s' % (self.password)
    def get_email(self):
        return '%s' % (self.email)

class UserManager():
    def __init__(self):
        client = get_client()

    def create_user(self, username, password, email):
        self.add_user( User(username, password, email) )
    
    def add_user(self, user):
        client = get_client()
        user_entity = self.user_to_entity(user)
        client.put(user_entity)
    
    def check_user(self, username):
        client = get_client()
        query = client.query(kind='Test1')

        for entity in query.fetch():
            fetch_username = self.entity_to_username(entity)
            if fetch_username == username:
                return True
        return False
    
    def check_email(self, email):
        client = get_client()
        query = client.query(kind='Test1')

        for entity in query.fetch():
            fetch_email = self.entity_to_email(entity)
            if fetch_email == email:
                return True
        return False
    
    def check_login(self, username, password):
        client = get_client()
        query = client.query(kind='Test1')

        for entity in query.fetch():
            fetch_username = self.entity_to_username(entity)
            fetch_password = self.entity_to_password(entity)
            
            if (fetch_username == username) and (fetch_password == password):
                return True
        return False



    
    
    def user_to_entity(self, user):
        client = get_client()
        key_user = client.key('Test1')

        user_store = datastore.Entity(key = key_user)
        user_store["username"] = user.get_username()
        user_store["password"] = user.get_password()
        user_store["email"] = user.get_email()
        return user_store
    
    def entity_to_username(self, user_entity):
        username = user_entity["username"]
        return username
    
    def entity_to_password(self, user_entity):
        password = user_entity["password"]
        return password

    def entity_to_email(self, user_entity):
        email = user_entity["email"]
        return email


    

import datetime
import flask
from google.cloud import datastore
from flask import request

def get_client():
    return datastore.Client()

class Review():
    def __init__(self, user, restaurant, order, wait, stars, text):
        self.user = user
        self.restaurant = restaurant
        self.order = order
        self.wait = wait
        self.stars = stars
        self.text = text
    
    def get_user(self):
        return '%s' % (self.user)
    def get_rest(self):
        return '%s' % (self.restaurant)
    def get_order(self):
        return '%s' % (self.order)
    def get_wait(self):
        return '%s' % (self.wait)
    def get_stars(self):
        return '%s' % (self.stars)
    def get_text(self):
        return '%s' % (self.text)

class ReviewManager():
    def __init__(self):
        client = get_client()

    def create_review(self, user, rest, order, wait, stars, text):
        self.add_review( Review(user, rest, order, wait, stars, text) )
    
    def add_review(self, review):
        client = get_client()
        review_entity = self.review_to_entity(review)
        client.put(review_entity)
    
    def reviews_filter_restaurant(self, restaurant):
        result = []
        client = get_client()
        query = client.query(kind='ReviewTest1')

        for entity in query.fetch():
            if self.entity_to_restaurant(entity) == restaurant:
                result.append(entity)       
                
        return result

 
    def review_to_entity(self, review):
        client = get_client()
        key_review = client.key('ReviewTest1')

        review_store = datastore.Entity(key = key_review)
        review_store["user"] = review.get_user()
        review_store["restaurant"] = review.get_rest()
        review_store["order"] = review.get_order()
        review_store["wait"] = review.get_wait()
        review_store["stars"] = review.get_stars()
        review_store["text"] = review.get_text()
        return review_store
    
    def entity_to_username(self, review_entity):
        username = review_entity["user"]
        return username
    
    def entity_to_restaurant(self, review_entity):
        restaurant = review_entity["restaurant"]
        return restaurant

    def entity_to_order(self, review_entity):
        order = review_entity["order"]
        return order

    def entity_to_wait(self, review_entity):
        wait = review_entity["wait"]
        return wait

    def entity_to_stars(self, review_entity):
        stars = review_entity["stars"]
        return stars
    
    def entity_to_text(self, review_entity):
        text = review_entity["text"]
        return text
    


    

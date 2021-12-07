from datetime import datetime
import flask
from google.cloud import datastore
from flask import request

def get_client():
    return datastore.Client()

class Review():
    def __init__(self, user, restaurant, order, wait, stars, text, favorite, time = None):
        self.user = user
        self.restaurant = restaurant
        self.order = order
        self.wait = wait
        self.stars = stars
        self.text = text
        self.favorite = favorite
        self.time = datetime.now()
    
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
    def get_favorite(self):
        return '%s' % (self.favorite)
    def get_time(self):
        """Return this messages's time as a 'YYYYMMDD HH:MM:SS' string."""
        return self.time.strftime('%Y%m%d %H:%M:%S')


class ReviewManager():
    def __init__(self):
        client = get_client()

    def create_review(self, user, rest, order, wait, stars, text, favorite):
        self.add_review( Review(user, rest, order, wait, stars, text, favorite) )
    
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
    
    def reviews_filter_recent(self, user):
        result = []
        client = get_client()
        query = client.query(kind='ReviewTest1')

        for entity in query.fetch():
            if self.entity_to_username(entity) == user:
                result.append(entity)       
        
        #sortedArray = sorted(result,key=lambda x: datetime.strptime(x['time'], '%m/%d/%y %H:%M'), reverse=True)
        #for entity in sortedArray:
        #    print(entity['restaurant'])
        result.reverse()
        return result
    
    def reviews_filter_favorite(self, user): 
        result = []
        check_rest = []
        client = get_client()
        query = client.query(kind='ReviewTest1')
        for entity in query.fetch():
            if self.entity_to_fav(entity) == "True" and self.entity_to_username(entity) == user and self.entity_to_restaurant(entity) not in check_rest:
                result.append(entity)      
                check_rest.append( self.entity_to_restaurant(entity) )
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
        review_store["favorite"] = review.get_favorite()
        review_store["time"] = review.get_time()
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
    
    def entity_to_fav(self, review_entity):
        fav = review_entity["favorite"]
        return fav
    
    def entity_to_time(self, review_entity):
        time = review_entity["time"]
        return time


    

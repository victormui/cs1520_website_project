import datetime
import flask
import user
import reviews
from flask import request, session, redirect, url_for


app = flask.Flask(__name__)
app.secret_key = "super secret key"
user_m = user.UserManager()
review_m = reviews.ReviewManager()

@app.route("/")
def route():
    return flask.render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    user = flask.request.form['username']
    pw = flask.request.form['password']

    if not(user_m.check_login(user, pw)):
        return flask.render_template('login.html', page_error = "Error: Username and password combination is incorrect", page_success = "Test")

    session['user'] = user
    return redirect(url_for('home_page'))


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    user = flask.request.form['username']
    pw = flask.request.form['password']
    email = flask.request.form['email']

    if user_m.check_email(email):
        return flask.render_template('login.html', page_error = "Error: E-Mail already in use.")
    if user_m.check_user(user):
        return flask.render_template('login.html', page_error = "Error: Username already in use.")
    
    user_m.create_user(user, pw, email)
    return flask.render_template('login.html', page_success = "Signed up successfully!")

@app.route("/add_review", methods=['GET', 'POST'])
def add_reviews():
    user = session['user']
    restaurant = flask.request.form['restaurant']
    order = flask.request.form['order']
    wait = flask.request.form['wait']
    rating = flask.request.form['rate']
    text = flask.request.form['user_review']

    review_m.create_review(user, restaurant, order, wait, rating, text)
    return redirect(url_for('render_reviews'))

@app.route("/all_reviews", methods=['GET', 'POST'])
def render_reviews():    
    #Chipotle
    chipotle = review_m.reviews_filter_restaurant("Chipotle")    
    #Five Guys
    five_guys = review_m.reviews_filter_restaurant("Five Guys")
    #Noodles n Co
    noodles_n_co = review_m.reviews_filter_restaurant("Noodles and Company")
    #Roots
    roots = review_m.reviews_filter_restaurant("Roots")
    #Primanti Bros
    primanti = review_m.reviews_filter_restaurant("Primanti Bros. Restaurant and Bar")
    #The Porch
    porch = review_m.reviews_filter_restaurant("The Porch at Schenley")
    #Chikn
    chikn = review_m.reviews_filter_restaurant("ChiKn")
    #Piada
    piada = review_m.reviews_filter_restaurant("Piada Italian Street Food")
    #McDonalds
    mcdonalds = review_m.reviews_filter_restaurant("McDonalds")
    #Subway
    subway = review_m.reviews_filter_restaurant("Subway")
    #Stackd
    stackd = review_m.reviews_filter_restaurant("Stack'd Oakland")
    #Oishii
    oishii = review_m.reviews_filter_restaurant("Oishii Bento")
    #Fuel and fuddle
    f_n_f = review_m.reviews_filter_restaurant("Fuel and Fuddle")
    #hello bistro
    h_bistro = review_m.reviews_filter_restaurant("Hello Bistro")

    return flask.render_template('review.html', chipotle = chipotle, five_guys = five_guys)

@app.route("/home", methods=['GET', 'POST'])
def home_page():
    return flask.render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

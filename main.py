from datetime import datetime
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
        return flask.render_template('login.html', page_error = "Error: Username and password combination is incorrect")

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
    if not session:
        return redirect(url_for('route'))
    user = session['user']
    restaurant = flask.request.form['restaurant']
    print("R S")
    order = flask.request.form['order']
    print("O S")
    wait = flask.request.form['wait']
    print("W S")
    rating = flask.request.form['rate']
    print("RA S")
    text = flask.request.form['user_review']
    print("U S")
    favorite = flask.request.form['favorite']
    print("F S")


    if favorite == "true":
        review_m.create_review(user, restaurant, order, wait, rating, text, True)
    else:
        review_m.create_review(user, restaurant, order, wait, rating, text, False)

    return redirect(url_for('render_reviews'))

@app.route("/all_reviews", methods=['GET', 'POST'])
def render_reviews():
    if not session:
        return redirect(url_for('login')) 
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
    the_porch = review_m.reviews_filter_restaurant("The Porch at Schenley")
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
    hello_bistro = review_m.reviews_filter_restaurant("Hello Bistro")

    return flask.render_template('review.html', chipotle = chipotle, five_guys = five_guys, 
    noodles_n_co = noodles_n_co, roots = roots, primanti = primanti, the_porch = the_porch, 
    chikn = chikn, piada = piada, mcdonalds = mcdonalds, subway = subway, stackd = stackd,
    oishii = oishii, f_n_f = f_n_f, hello_bistro = hello_bistro)

@app.route("/home", methods=['GET', 'POST'])
def home_page():
    if not session:
        return redirect(url_for('route'))
        
    get_favorited = review_m.reviews_filter_favorite(session['user'])
    get_recent = review_m.reviews_filter_recent(session['user'])

    if not get_favorited and not get_recent:
        return flask.render_template('home.html',no_fav = "No restaurants favorited", no_recent = "No recent restaurants")
    elif not get_recent:
        return flask.render_template('home.html',no_recent = "No recent restaurants", favs = get_favorited)
    elif not get_favorited:
        return flask.render_template('home.html',no_fav = "No restaurants favorited", recent = get_recent)

    return flask.render_template('home.html', favs = get_favorited, recent = get_recent)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('route'))

@app.route("/reviews", methods=['GET', 'POST'])
def get_specific_review():
    if not session:
        return redirect(url_for('route'))
    restaurant = flask.request.form['restaurant']


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

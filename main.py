import datetime
import flask
import user
from flask import request, session


app = flask.Flask(__name__)
user_m = user.UserManager()

@app.route("/")
def route():
    return flask.render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    user = flask.request.form['username']
    pw = flask.request.form['password']

    if not(user_m.check_login(user, pw)):
        return flask.render_template('login.html', page_error = "Error: Username and password combination is incorrect")

    return flask.render_template('home.html')


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

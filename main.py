import datetime
import flask
import message



app = flask.Flask(__name__)

@app.route('/')
def route():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

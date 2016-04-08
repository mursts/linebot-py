from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/bot/callback')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

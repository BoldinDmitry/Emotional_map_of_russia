#!flask/bin/python
from flask import Flask

app = Flask(__name__)


@app.route('/cities')
def get_tasks():
    f = open("cities.json", "r").read()
    return f


if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/python3
"""
start a Flask web application
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' on the main route."""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

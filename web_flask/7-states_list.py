#!/usr/bin/python3
"""
start a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' on the main route."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Returns HBNB from on the hbnb route. """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Returns hbnb route """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """Display python is cool with the value of the text """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Display n is a number only if n is an integer. """
    return '{} is a number'.format(n)


@app.route('/number_templates/<int:n>', strict_slashes=False)
def number_template(n):
    """Display a html page only if n is an integer."""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Display a html page only if n is an integer indicating """
    return render_template('6-number_odd_or_even.html', n=n)


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLALchemy Session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of all state objects present in DBSstorage"""
    states = storage.all(State).values()
    print("Number of states:", len(states))  # Add this line for debugging
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=states_sorted)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

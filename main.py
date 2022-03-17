from flask import Blueprint, render_template


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search')
def search():
    return 'Search'
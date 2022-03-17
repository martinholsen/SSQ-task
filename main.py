from flask import Blueprint, redirect, render_template, url_for, request


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/', methods=['POST'])
def index_post():
    q = request.form.get('query')

    return redirect(url_for('main.search'))

@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/search', methods=['POST'])
def search_post():

    return render_template('search.html')

from flask import Flask, redirect, render_template, request, url_for
import pandas as pd

app = Flask(__name__)

# Route for index page
@app.route("/")
def index():
    return redirect(url_for('search'))

# Route for search page
@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')
    
with app.test_request_context():
    print(url_for('index'))
    print(url_for('search'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
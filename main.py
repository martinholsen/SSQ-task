from flask import Blueprint, redirect, render_template, url_for, request
import requests
import pandas as pd
import io


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/', methods=['POST'])
def index_post():
    # Query management from end user
    q = request.form.get('query')
    api_url = 'https://hotell.difi.no/api/csv/mattilsynet/smilefjes/tilsyn?'
    q = 'query=' + q
    query = api_url+q

    # Establish dataframe and send request to databank
    df = pd.DataFrame()
    data = io.StringIO(requests.get(query).text)    # Line converts request response object to raw text and then to a text buffer for pandas
    df = pd.read_csv(data, sep='delimiter', header=None, encoding='utf-8')  # Reads text buffer as CSV file
    df = df.reset_index()   # making sure indexes pair with number of rows

    clear_restaurants()     # Empty current buffer
    create_restaurants()    # A dictionary of restaurants that is filled with only relevant data from the query
    
    for index, row in df.iterrows():
        if not index:
            continue    # simply ignore the first indexed row as it contains only metadata
        if type(row[0]) is not str:
            continue
        templist = list(row[0].split(';'))
        templist = [entry.strip().title().strip('"') for entry in templist]
        if len(templist) < 25:  # Remove invalid lists
            continue
        
        # Manual datagrab
        navn = templist[7]
        dato = templist[6]
        tlf = templist[4]
        fylke = templist[1]
        k1 = scale_score(templist[14])
        k2 = scale_score(templist[16])
        k3 = scale_score(templist[17])
        k4 = scale_score(templist[18])
        tot = scale_score(templist[19])

        if navn in restaurants:
            if restaurants.get(navn).get('dato') > dato:    # If an entry with the same name and older date is found ignore it
                continue    
        
        tempdict = {'dato': dato, 'Tlf': tlf, 'Fylke': fylke, 'Karakter-1': k1, 'Karakter-2': k2, 'Karakter-3': k3, 'Karakter-4': k4,
        'Total': tot}
        restaurants.update({navn: tempdict})    # Restaurants dict is updated and is a dictonary with key: value pairs of restaurant names and relevant info
        
        

    return redirect(url_for('main.search'))

@main.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    return render_template('search.html', restaurants=restaurants)

@main.route('/search', methods=['POST'])
def search_post():
    # Query management from end user
    q = request.form.get('query')
    api_url = 'https://hotell.difi.no/api/csv/mattilsynet/smilefjes/tilsyn?'
    q = 'query=' + q
    query = api_url+q

    # Establish dataframe and send request to databank
    df = pd.DataFrame()
    data = io.StringIO(requests.get(query).text)    # Line converts request response object to raw text and then to a text buffer for pandas
    df = pd.read_csv(data, sep='delimiter', header=None, encoding='utf-8')  # Reads text buffer as CSV file
    df = df.reset_index()   # making sure indexes pair with number of rows

    clear_restaurants()     # Empty current buffer
    create_restaurants()    # A global dictionary of restaurants to be filled with only relevant data from the query
    
    for index, row in df.iterrows():
        if not index:   # simply ignore the first indexed row as it contains only metadata
            continue
        if type(row[0]) is not str:
            continue
        templist = list(row[0].split(';'))
        templist = [entry.strip().title().strip('"') for entry in templist]
        if len(templist) < 25:  # Remove invalid lists
            continue

        # Manual datagrab
        navn = templist[7]
        dato = templist[6]
        tlf = templist[4]
        fylke = templist[1]
        k1 = scale_score(templist[14])
        k2 = scale_score(templist[16])
        k3 = scale_score(templist[17])
        k4 = scale_score(templist[18])
        tot = scale_score(templist[19])

        if navn in restaurants:
            if restaurants.get(navn).get('dato') > dato:    # If an entry with the same name and older date is found ignore it
                continue                                    
        
        tempdict = {'dato': dato, 'Tlf': tlf, 'Fylke': fylke, 'Karakter-1': k1, 'Karakter-2': k2, 'Karakter-3': k3, 'Karakter-4': k4,
        'Total': tot}
        restaurants.update({navn: tempdict})    # Restaurants dict is updated and is a dictonary with key: value pairs of restaurant names and relevant info

    return render_template('search.html', restaurants=restaurants)

def create_restaurants():   # Make global buffer
    global restaurants
    if 'restaurants' not in globals():
        restaurants = {}

def clear_restaurants():    # Clear buffer
    if 'restaurants' in globals():
        restaurants.clear()

def scale_score(score=None):    # Convert int score to readable assessment
    if not score.isdigit():
        return
    vurderinger = ['Utmerket', 'Bra', 'Passe', 'Dårlig', 'Ikke aktuelt', 'Ikke vurdert']
    return vurderinger[int(score)]  # returns assessment based on score system between 0-5


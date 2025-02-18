from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from pymongo import MongoClient
from utils import process

app = Flask(__name__)
CORS(app)
app.secret_key = 'etjo6uyjkl'

client = MongoClient('mongodb://localhost:27017/sign')
db = client['auth_db']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('home.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username, 'password': password})
        
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('verify'))  
        else:
            flash('Invalid credentials, please try again.', 'error') 
            return redirect(url_for('login'))  
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if users_collection.find_one({'username': username}):
            return render_template('signup.html', error='Username already exists, please choose another.')
        
        users_collection.insert_one({'username': username, 'password': password})
        
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('verify'))  
    
    return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  
    return redirect(url_for('index'))  

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  

    note = ''
    if request.method == 'POST':
        if 'image1' not in request.files or 'image2' not in request.files:
            note = 'Please upload both images.'
        else:
            image1 = request.files['image1'].read()
            image2 = request.files['image2'].read()

            if not image1 or not image2:
                note = 'Please upload valid images.'
            else:
                res = process(image1, image2)
                note = 'Forged Signature' if res == 1 else 'Real Signature'

    return render_template('verify.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from utils import process

app = Flask(__name__)
CORS(app)

# Secret key for session management
app.secret_key = 'etjo6uyjkl'

# Dummy storage for user credentials (this should be replaced with a database in production)
users = {}

@app.route('/')
def index():
    return render_template('home.html')  # Render the home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']     

        # Check if user exists and the password is correct
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('verify'))  # Redirect to the verification page
        else:
            flash('Invalid credentials, please try again.', 'error')  # Flash message for login failure
            return redirect(url_for('login'))  # Re-render login page with error message

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return render_template('signup.html', error='Username already exists, please choose another.')

        # Add the new user to the 'users' dictionary
        users[username] = password

        # Automatically log in the user after signup
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('verify'))  # Redirect directly to the verification page after signup

    return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Clears the session data
    return redirect(url_for('index'))  # Redirect to home page after logout

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

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
                # Process the images
                res = process(image1, image2)
                note = 'Forged Signature' if res == 1 else 'Real Signature'

    return render_template('verify.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)

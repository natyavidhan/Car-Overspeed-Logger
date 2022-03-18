from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from dotenv import load_dotenv
from databases import Database
import os

if os.path.exists('.env'):
    load_dotenv('.env')

app = Flask(__name__)
app.secret_key = os.environ.get('secret')
database = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error=None)
    else:
        email, password = request.form['email'], request.form['password']
        user = database.authenticate(email, password)
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid email or password')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', error=None)
    else:
        email, password, name = request.form['email'], request.form['password'], request.form['name']
        user = database.registerUser(email, password, name)
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        return render_template('register.html', error='Invalid email or password')

if __name__ == '__main__':
    app.run(debug=True)
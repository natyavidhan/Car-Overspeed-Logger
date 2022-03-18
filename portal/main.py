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
    if 'user' in session:
        return redirect(url_for('dashboard'))
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
    
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        title, content = request.form['title'], request.form['content']
        database.reportFromPortal(session['user']['_id'], title, content)
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
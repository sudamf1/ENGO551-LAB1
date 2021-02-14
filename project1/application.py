import os

from flask import Flask, session, render_template,url_for,request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: HALO"

@app.route('/login',methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST': 
        if request.form['username'] != 'admin' or request.form['password'] != 'admin' :
            error = 'Wrong username or Password, please try again'
            
        else: 
            return redirect(url_for('index'))
    return render_template('login.html', error = error)
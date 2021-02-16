import os

from flask import Flask, session, render_template,url_for,request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import cast
import datetime


# class username: 
#     def _init_(self,id,username,password): 
#         self.id = id
#         self.username = username
#         self.password = password
        
#     def _repr_(self):
#         return f'<user:{self.username}>'

# users = []
# users.append(username(id =1, username = 'sudam',password = 'sudam123'))

 
app = Flask(__name__, template_folder = 'templates')



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem

# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine("postgres://dlfgudwjehlelv:522a0e4845ba7861a358d35d55039bfa4c1a13997c0525b87443ba9638d2a7bf@ec2-52-205-3-3.compute-1.amazonaws.com:5432/dcvm5r8h0eivr8"
)
db = scoped_session(sessionmaker(bind=engine))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dlfgudwjehlelv:522a0e4845ba7861a358d35d55039bfa4c1a13997c0525b87443ba9638d2a7bf@ec2-52-205-3-3.compute-1.amazonaws.com:5432/dcvm5r8h0eivr8"
app.config["SESSION_TYPE"] = False
db = SQLAlchemy(app)
db.init_app(app)


class User(db.Model) :
    
    __tablename__ = "User"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(127), unique = True, nullable = False)
    password = db.Column(db.String(127), nullable = False)
    
    db.create_all()
    # def __init__(self,id,username,password):
    #     self.id = id
    #     self.username = username
    #     self.password = password




@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/Home")
def Home():
    return render_template ("Home.html")

@app.route('/login', methods = ['GET','POST'])
def login():
   
    if request.method == 'POST': 
        session['username'] = request.form.get("username")
        session['password'] = request.form.get("password")
        
        check = User.query.filter(User.username.like(session.get('username'))).first()
        
    else :
        session['logged_in'] = True
        return render_template("Home.html")
        
           
    return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():

        username = request.form.get("username")
        password = request.form.get("password")
    
        check = User.query.filter_by(username = username).first()
       
        if check == None:
            new_user = User(username = username, password = password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        return render_template('registration.html', name = username)
    
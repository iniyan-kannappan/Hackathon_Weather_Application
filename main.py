from flask import Flask, redirect, render_template, url_for, request
from flask_login import login_user,login_required,logout_user
from forms import LoginForm,RegistrationForm
from weather import weather_api
from forms import Form
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

# Used in in-built flask auth
login_manager=LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# To create your base directory
# __file__ --> main.py
basedir=os.path.abspath(os.path.dirname(__file__))

# Creates a Flask application
app=Flask(__name__)

# Creates a SQLAlchemy Database
db=SQLAlchemy(app)

# Creates a Model for the Database
class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True, index=True)
    username=db.Column(db.String(64),unique=True, index=True)
    password_hash=db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)


    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

# Configures the app, database, and modifications
app.config['SECRET_KEY']='mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Will migrate the database
Migrate(app,db)
login_manager.init_app(app)
login_manager.login_view='login'

# View for homepage
@app.route('/',methods=['GET', 'POST'])
def index():
    form=Form()
    if form.validate_on_submit():
        weather=weather_api(form.zip.data)
        nec={'description':weather['weather'][0]['description'],
             'temp':weather['main']['temp'],
             'temp_min':weather['main']['temp_min'],
             'temp_max':weather['main']['temp_max'],
             'name':weather['name']}
        return render_template('home.html',nec=nec)
    return render_template('home.html',form=form)

# View for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# View for login
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        print('User is ',user.username)
        if user.check_password(form.password.data) and user != None:
            login_user(user)
            next=request.args.get('next')

            if next == None or not next[0]=='/':
                next=url_for('index')
            return redirect(next)
    return render_template('login.html',form=form)

# View for register
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

# For Running the application
if __name__ == '__main__':
    app.run(debug=True)
import os
# To grab directory names and file path names
from flask import Flask, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from weather import weather_api
import requests
import json
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# basedir=os.path.abspath(os.path.dirname(__file__))
# To create your base directory
# __file__ --> basic.py

app=Flask(__name__)

app.config['SECRET_KEY']='mysecretkey'

class Form(FlaskForm):
    zip=StringField('What is your zip code?')
    submit=SubmitField('Submit')

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
# # To connect the Flask application to the database
# 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# 
# db=SQLAlchemy(app)
# 
# Migrate(app, db)

@app.route('/',methods=['GET', 'POST'])
def index():
    form=Form()
    if form.validate_on_submit():
        print(weather_api(form.zip.data))
        return redirect(url_for('index'))
    return render_template('home.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FinalProject import app
from os import path
from datetime import datetime
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from FinalProject.Models.Forms import ExpandForm
from FinalProject.Models.Forms import CollapseForm
from os import path
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
#db_Functions = create_LocalDatabaseServiceRoutines()

import pandas as pd
app.config['SECRET_KEY'] = 'bla bla'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/database')
def database():
    """Renders the database page."""
    return render_template(
        'database.html',
        title='מאגר הנתונים',
        year=datetime.now().year,
        message='כאן יתואר מאגר הנתונים של העושר עולמי .'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/data/HappinessData' , methods = ['GET' , 'POST'])
def HappinessData():

    print("HappinessData")
    form1 = ExpandForm()
    form2 = CollapseForm()


    """Renders the about page."""
    # data = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\HappinessData.csv'))
    data = pd.read_csv(path.join(path.dirname(__file__), 'static/data/HappinessData.csv'))
    raw_data_table = ''
    raw_data_table = data.to_html(classes = 'table table-hover')    

    return render_template(
        'data.html',
        title='Happiness data',
        year=datetime.now().year,
        message='My data page.',
        raw_data_table = raw_data_table
        ,
        form1 = form1,
        form2 = form2

    )

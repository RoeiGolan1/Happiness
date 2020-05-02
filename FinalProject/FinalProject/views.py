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
from FinalProject.Models.Forms import HapinessForm
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
        title='Roei Golan - רועי גולן',
        year=datetime.now().year,
        message='My contact page.'
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
        year=datetime.now().year,
      
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
@app.route('/Query' , methods = ['GET' , 'POST'])
def query():

    print("Query")

    form1 = HapinessForm()
    chart = ''

   
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/HappinessData.csv'))
    country_list = list(df["Country or region"])
    chices = list(zip(country_list, country_list))
    form1.parmeter1.choices = chices
    form1.parmeter2.choices = chices
    col_name = list(df.columns)
    parmeters_choices = list(zip(col_name, col_name))
    form1.countries.choices = parmeters_choices
    
    if request.method == 'POST':
        parmeter1= form1.parmeter1.data
        parmeter2= form1.parmeter2.data
        country_list = form1.countries.data
        df=df[[parmeter1, parmeter2]]
        df=df.set_index("Country or region")
        df=df.loc[contry_list]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        df.plot(ax = ax , kind = 'bar', figsize = (24, 8) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

    
    return render_template(
        'query.html',
        form1 = form1,
        chart = chart
    )
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

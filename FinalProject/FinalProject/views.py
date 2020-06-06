"""
Routes and views for the flask application.
"""
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from FinalProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
import io
from datetime import datetime
from flask import render_template
from FinalProject import app
from os import path
from datetime import datetime
from flask import render_template
from flask import request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from FinalProject.Models.Forms import ExpandForm
from FinalProject.Models.Forms import CollapseForm
from FinalProject.Models.Forms import HapinessForm
from FinalProject.Models.Forms import UserRegistrationFormStructure
from FinalProject.Models.Forms import LoginFormStructure
from os import path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
db_Functions = create_LocalDatabaseServiceRoutines()
#imports
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
    #reads csv
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/HappinessData.csv'))
    raw_data_table = ''
    #if the user presses submit
    if request.method == 'POST':
        #if the user clicks on expand the data base will now be shown on the page
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        #if the user clicks on collapse the data base will be removed
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

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
    form1.countries.choices = chices
    col_name = list(df.columns)
    parmeters_choices = list(zip(col_name, col_name))
    print(parmeters_choices)
    parmeters_choices.pop(0)
    parmeters_choices.pop(0)
    print(parmeters_choices)
    form1.parmeter1.choices = parmeters_choices
    form1.parmeter2.choices = parmeters_choices
    #saves choices for categories for queries
    if request.method == 'POST':
        parmeter1= form1.parmeter1.data
        parmeter2= form1.parmeter2.data
        country_list = form1.countries.data
        df=df[["Country or region"] + [parmeter1, parmeter2]]
        df=df.set_index("Country or region")
        df=df.loc[country_list]
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
#creates graph for query
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )
 

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

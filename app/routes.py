from flask import render_template
from app import app
from app.forms import LoginForm


#Decorator modifies the fxn it follows, the @app.route decorator
#creates an association bt URL given as an argument & the fxn.
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'NjiChe.dev'}

    posts = [
        {
            'author':{'username': 'Fru'},
            'body': 'beatiful day in Buea'
        },
        {
            'author':{'username': 'Ngum'},
            'body': 'The space between us was awesome'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

#renderinng is the process that converts a template in2 a HTMl page
#This is done by imporx the inbuilt render_template() fxn
#this fxn takes a template filename & a varibale list of template
#Arguments and return it w the placeholders replaced with actual values

#the render template() invokes the jinja template engine that comes
#with flask

#Jinja aslo supports control statements given inside {%---%}

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
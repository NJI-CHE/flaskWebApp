from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User



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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#renderinng is the process that converts a template in2 a HTMl page
#This is done by imporx the inbuilt render_template() fxn
#this fxn takes a template filename & a varibale list of template
#Arguments and return it w the placeholders replaced with actual values

#the render template() invokes the jinja template engine that comes
#with flask

#Jinja aslo supports control statements given inside {%---%}

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me{}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@pp.route('logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
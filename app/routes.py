from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
from  datetime import datetime, timezone
from app.forms import EditProfileForm
from flask import abort



#Decorator modifies the fxn it follows, the @app.route decorator
#creates an association bt URL given as an argument & the fxn.
@app.route('/')
@app.route('/index')
@login_required
def index():
    #user = {'username': 'NjiChe.dev'}

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
    return render_template('index.html', title='Home', posts=posts)

@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')

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
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)



#renderinng is the process that converts a template in2 a HTMl page
#This is done by imporx the inbuilt render_template() fxn
#this fxn takes a template filename & a varibale list of template
#Arguments and return it w the placeholders replaced with actual values

#the render template() invokes the jinja template engine that comes
#with flask

#Jinja aslo supports control statements given inside {%---%}

#@app.route('/login',methods=['GET', 'POST'])
#def login():
    #form = LoginForm()
    #if form.validate_on_submit():
       # flash('Login requested for user {}, remember_me{}'.format(form.username.data, form.remember_me.data))
        #return redirect(url_for('index'))
    #return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

#Creating user profiles, so we create a route for specific user profiles, the route decorato has a dynamic component in 'username' which sets to the particular
#username of a user when called,
#@login_required- ensures only loginn users are going to have access
#we first try to load user from db using query by username; the db.first_or_404 send result if available or returns  a 404 error if db is empty

@app.route('/user/<username>')
#@login_required
def user(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        abort(404)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


#View function for the EditProfile
@app.route('/edit_profile', methods=['GET', 'POST'])
#@login_required
def edit_profile():
    form= EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return  render_template('edit_profile.html', title='Edit Profile', form=form)


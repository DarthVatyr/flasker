from flask import Flask, render_template, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Set the Secret Key
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize the database
db = SQLAlchemy(app)

# Create a model
class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), nullable=False, unique=True)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  # Create a string
  def __repr__(self):
    return '<Name %r>' % self.name

with app.app_context():
    db.create_all()

#To push a context manually, using a plain python shell.
#$ python
#>>> from project import app, db
#>>> app.app_context().push()
#>>> db.create_all()

# Create a form class
class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create a form class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#These are common Jinja filters to use with the variables passed to our html templates
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags
#

@app.route('/user/add', methods=["GET", "POST"])
def add_user():
  name = None
  form = UserForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      user = Users(name=form.name.data, email=form.email.data)
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.name.data = ''
    form.email.data = ''
    flash("User Added Successfully")
  our_users = Users.query.order_by(Users.date_added)
  return render_template('add_user.html', form=form, name=name, our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
  first_name = 'Josh'
  stuff = "This is <strong>bold</strong> text"
  pizza = ["pepperoni", "cheese", "sausage", 10]
  return render_template('index.html', first_name=first_name, stuff=stuff, pizza=pizza)

# Create a route decorator
@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)

# Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_foun(error):
  return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html'), 500

# Create a name page
@app.route('/name', methods=["GET", "POST"])
def name():
  name = None
  form = NameForm()
  # Validate the form
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
    flash("Form Submitted Successfully!")
  return render_template('name.html', name=name, form=form)

# Run the Flask App
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
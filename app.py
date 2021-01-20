from flask import Flask, render_template, request,flash, url_for 
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from covid import coverd_obj
import random
from  datetime import  datetime
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_login import LoginManager, login_required ,UserMixin, login_user, logout_user, current_user

from form import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SECRET_KEY'] = "your-secret-key-here"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app) 



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True )
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return '<User %r>' % self.email

class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text ,nullable=False)
    price = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    Acourse = Course.query.all()
    return render_template('home.html',Acourse=Acourse)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash("Successful Login")
            return redirect(url_for('home'))
        else:
            flash("Invalid Login")
    else:
        pass
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create-course',methods=["GET", "POST"])
def create():

    if request.method == "POST":

        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        obj = Course(title=title,
                     instructor=instructor,
                     price=price,
                     duration=duration,
                     description=description)

        db.session.add(obj)
        db.session.commit()

    return render_template('create-course.html')

@app.route('/covid-table')
def covid_table():

    covid_data  = coverd_obj
    
    return render_template('covid-table.html',covid_data=covid_data)


@app.route('/covid-dashboad')
def covid_dashboad():

    data = coverd_obj
    data_confirmed = data["Confirmed"]
    data_recovered = data["Recovered"]
    data_updatedate = data["UpdateDate"]
    data_hospitalized = data["Hospitalized"]
    data_newdeaths = data["NewDeaths"]
    data_newconfirmed = data["NewConfirmed"]
    return render_template('covid-dashboad.html', data1=data_confirmed,data2=data_recovered,data_updatedate=data_updatedate,data3=data_hospitalized,data4=data_newdeaths,data5=data_newconfirmed)

@app.route('/post/<int:id>')
def post(id):
    course = Course.query.get(id)
    return render_template('post.html',course=course)

@app.route('/random-menu')
def random_menu():
    random_list =["กระเพรา","ไข่เจียว","ก๋วยเตี๋ยว"]
    menu_data = random.choice(random_list)

    return render_template('random-menu.html',menu_data=menu_data)

@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):

    data = Course.query.get(id)
    if request.method == "POST":
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        data.title = title
        data.instructor = instructor
        data.price = price
        data.duration = duration
        data.description = description

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update.html',data=data)

@app.route('/delete/<int:id>',methods=["GET", "POST"])
def delete(id):

    data = Course.query.get(id)

    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/sign-up',methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        

        obj = User(username=username,password=generate_password_hash(password,method=('sha256')),email=email)

        db.session.add(obj)
        db.session.commit()
        return render_template('home.html')
    return render_template('sign-up.html')


if __name__ == '__main__':
    app.run(debug=True)

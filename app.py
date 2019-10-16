from flask import Flask , render_template,flash,request,redirect,url_for,session
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

from data import instance_status

app = Flask(__name__)

#Intialize URI for SQLLite DB for SQLALCHMEY

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'

#Wraping flask app in SQLALCHEMY

db=SQLAlchemy(app)

instance_status=instance_status()

#SQLAlchmey mapping with SQLLite DB
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

# decorator to check login session
def is_loged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized Please login','danger')
            return  redirect(url_for('login'))
    return wrap

#URL Route Default
@app.route('/')
def index():
    return render_template('HOME.html')

# Registration Form creation
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.data_required(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm= PasswordField('Confirm Password')

#Route to Registration form

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=sha256_crypt.encrypt(str(form.password.data))

        registration = users(name=name, username=username, email=email, password=password)
        db.session.add(registration)
        db.session.commit()
        flash(' You are now registered .Your Username is: '+username,'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# Route to Login form
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username_login=request.form['username']
        password_candidate=request.form['password']


        results=users.query.filter_by(username=username_login).first()
        if results :
            password=results.password
            if sha256_crypt.verify(password_candidate,password):
                session['logged_in']=True
                session['username']=username_login

                flash('You are successfully logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error=error)
        else:
            error='User is not registered'
            return render_template('login.html',error=error)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',instance_status=instance_status)

@app.route('/instance_details/<string:id>', methods=['GET','POST'])
def instance_details(id):
    return render_template('instance_details.html',id=id)

#
@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out','success')
    return redirect(url_for('login'))





if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)
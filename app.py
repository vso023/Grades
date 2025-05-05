from flask import Flask, render_template, session, flash, redirect, url_for
from functools import wraps
import pymongo


app = Flask(__name__)

app.secret_key = "mysecretkey"

client = pymongo.MongoClient("mongodb+srv://valeriesofia0923:valeriesofia0923@grades.1t1soeq.mongodb.net/Grades")

db = client.Grades

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Debes iniciar sesion primero')
            return redirect('/')
    return wrap

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/perfil/')
@login_required
def perfil():
    return render_template('perfil.html')

from user import routes
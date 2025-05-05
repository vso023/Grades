from bson import ObjectId
from flask import render_template, redirect, url_for, request, jsonify, Flask, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from user.models import User
from app import login_required
from passlib.hash import pbkdf2_sha256

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
    
@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/register')
def show_register_form():
    return render_template('register.html')


@app.route('/user/login', methods=['POST'])
def login():
    
    email = request.form['email']
    password = request.form['password']


    # Buscar el usuario en la base de datos
    user = db.users.find_one({"email": email})

    print(user)

    if user and pbkdf2_sha256.verify(password, user['password']):
        return User().start_session(user)

    # Si las credenciales son incorrectas, mostrar mensaje de error
    return render_template("login.html", error="Credenciales incorrectas"), 401
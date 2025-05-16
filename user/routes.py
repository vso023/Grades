from bson import ObjectId
from flask import render_template, redirect, url_for, request, jsonify, Flask, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from user.models import User, Course
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
    
    code = request.form['code']
    password = request.form['password']


    # Buscar el usuario en la base de datos
    user = db.users.find_one({"code": code})

    print(user)

    if user and pbkdf2_sha256.verify(password, user['password']):
        return User().start_session(user)

    # Si las credenciales son incorrectas, mostrar mensaje de error
    return render_template("login.html", error="Credenciales incorrectas"), 401

@app.route('/create_course', methods=['GET','POST'])
@login_required
def create_course():
    title = request.form.get('title')
    description = request.form.get('description')
    user_id = session['user']['_id']

    if not title or not description:
        return render_template('create_course.html', error="Todos los campos son obligatorios")

    course = Course(title, description, user_id)
    if course.save():
        return redirect(url_for('dashboard'))
    else:
        return render_template('create_course.html', error="Error al crear el curso")
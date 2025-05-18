from bson import ObjectId
from flask import render_template, redirect, url_for, request, jsonify, Flask, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from user.models import User, Course, Activity, Topic
from app import login_required
import uuid
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


@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if not session.get('user'):
        return redirect('/login')

    if request.method == 'GET':
        # Devuelve la plantilla para crear curso (formulario)
        return render_template('create_course.html')

    # POST:
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    user_id = session['user']['_id']
    course_id = uuid.uuid4().hex
    topic_ids = []

    for topic in data['topics']:
        topic_id = uuid.uuid4().hex
        activity_ids = []

        for activity in topic['activities']:
            activity_id = uuid.uuid4().hex
            Activity.create_activity_with_id(
                activity_id=activity_id,
                title=activity['title'],
                description=activity['description'],
                weight=activity['weight'],
                links=activity.get('links', [])
            )
            activity_ids.append(activity_id)

        Topic.create_topic_with_id(
            topic_id=topic_id,
            title=topic['title'],
            description=topic['description'],
            activity_ids=activity_ids,
            corte=topic['corte'],           # <-- Aquí lo pasas
            links=topic.get('links', [])
        )

        topic_ids.append(topic_id)

    course = {
        "_id": course_id,
        "title": data['title'],
        "description": data['description'],
        "user_id": user_id,
        "topics": topic_ids
    }
    db.courses.insert_one(course)

    return jsonify({'success': True, 'course_id': course_id}), 200

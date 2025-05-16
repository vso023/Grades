from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def start_session(self, user):
        # Eliminar la contraseña antes de guardarla en la sesión
        
        print("Entro")
        
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return redirect(url_for('perfil'))  # Redirige al dashboard después de iniciar sesión
    
    def signup(self):
        # Imprimir los datos del formulario para depuración
        print("Form data:", request.form)

        # Validar que los campos necesarios estén presentes
        if not request.form.get('name') or not request.form.get('code') or not request.form.get('password'):
            return render_template("register.html", error="Todos los campos son obligatorios"), 400
        
        # Crear el objeto de usuario
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "last_name": request.form['last_name'],
            "code": request.form['code'],
            "phone_number": request.form['phone_number'],
            "email": request.form['email'],
            "password": request.form['password']
        }

        # Cifrar la contraseña
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Comprobar si el correo electrónico ya está en uso
        if db.users.find_one({"email": user['email']}):
            return render_template("register.html", error="Correo ya está en uso"), 400
        
        if db.users.find_one({"code": user['code']}):
            return render_template("register.html", error="Codigo ya está en uso"), 400
        
        if db.users.find_one({"phone_number": user['phone_number']}):
            return render_template("register.html", error="Numero telefonico ya está en uso"), 400

        # Intentar insertar el nuevo usuario en la base de datos
        try:
            result = db.users.insert_one(user)
            if result.inserted_id:
                # Si la inserción es exitosa, redirigir al login
                return redirect(url_for('dashboard'))
            else:
                return render_template("register.html", error="No se pudo registrar"), 400
        except Exception as e:
            # Capturar cualquier error que ocurra durante la inserción
            print("Error durante la inserción:", e)
            return render_template("register.html", error="Hubo un problema al intentar registrar al usuario"), 500
    
    def signout(self):
        # Limpiar la sesión
        session.clear()
        return redirect('/')

    def login(self):
        # Buscar al usuario en la base de datos
        user = db.users.find_one({"code": request.form['code']})

        # Verificar si el usuario existe y la contraseña es correcta
        if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
            # Iniciar sesión del usuario
            return self.start_session(user)
        
        # Si las credenciales son incorrectas, devolver un error
        return render_template("login.html", error="Credenciales incorrectas"), 401

class Course:
    def __init__(self, title, description, user_id):
        self.course = {
            "_id": uuid.uuid4().hex,
            "title": title,
            "description": description,
            "created_by": user_id
        }

    def save(self):
        try:
            db.courses.insert_one(self.course)
            return True
        except Exception as e:
            print("Error al guardar curso:", e)
            return False
from flask import Flask, render_template, session, flash, redirect, url_for
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = "mysecretkey"

# URI de conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://valeriesofia0923:valeriesofia0923@grades.1t1soeq.mongodb.net/?retryWrites=true&w=majority"

try:
    # Conectar a MongoDB con timeout de 5 segundos
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Verificar conexión (ping al servidor)
    client.admin.command("ping")
    print("✅ Conexión exitosa con MongoDB Atlas")
    
    db = client["Grades"]  # Seleccionar base de datos
except Exception as e:
    print("❌ Error al conectar con MongoDB Atlas:")
    print(e)
    db = None  # Evita errores si db se usa después sin conexión

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Debes iniciar sesión primero')
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

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Importa rutas del módulo user
from user import routes

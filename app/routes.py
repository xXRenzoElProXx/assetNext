from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import datetime
from flask_login import current_user

@app.route('/')
@login_required
def home():
    return render_template('index.html', usuario=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            error = 'Correo o contraseña incorrectos.'
    return render_template('login.html', error=error)



@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            error = 'Las contraseñas no coinciden.'
        else:
            # Verificar si el correo ya existe
            if Usuario.query.filter_by(email=email).first():
                error = 'El correo ya existe.'
            else:
                try:
                    fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
                except ValueError:
                    error = 'Fecha de nacimiento inválida.'
                    return render_template('register.html', error=error)
                hashed_password = generate_password_hash(password)
                new_user = Usuario(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/olvidarcontraseña', methods=['GET', 'POST'])
def olvidar_contraseña():
    error = None
    success = None
    if request.method == 'POST':
        email = request.form['email']
        # Aquí iría la lógica para enviar el correo de recuperación
        # Por ahora solo mostramos un mensaje de éxito si el email existe
        user = Usuario.query.filter_by(email=email).first()
        if user:
            success = 'Se han enviado instrucciones a tu correo.'
        else:
            error = 'El correo no está registrado.'
    return render_template('olvidarcontraseña.html', error=error, success=success)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

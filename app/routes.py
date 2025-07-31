from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import pytz
from flask_mail import Message, Mail

# Configurar zona horaria de Lima, Perú
LIMA_TZ = pytz.timezone('America/Lima')

# Configuración de mail con tus datos
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'assetnext.tech@gmail.com'
app.config['MAIL_PASSWORD'] = 'swgx tcqh lpcf tvwc'
app.config['MAIL_DEFAULT_SENDER'] = 'assetnext.tech@gmail.com'

mail = Mail(app)

@app.route('/')
@login_required
def home():
    # Actualizar última conexión
    current_user.ultima_conexion = datetime.datetime.now(LIMA_TZ)
    db.session.commit()
    return render_template('index.html', usuario=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            user.ultima_conexion = datetime.datetime.now(LIMA_TZ)
            db.session.commit()
            login_user(user)
            # Redirigir siempre a home, ignorando el parámetro 'next'
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
        
        if password != confirm_password:
            error = 'Las contraseñas no coinciden.'
        else:
            if Usuario.query.filter_by(email=email).first():
                error = 'El correo ya existe.'
            else:
                try:
                    fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
                except ValueError:
                    error = 'Fecha de nacimiento inválida.'
                    return render_template('register.html', error=error)
                
                hashed_password = generate_password_hash(password)
                new_user = Usuario(
                    nombre=nombre, 
                    apellido=apellido, 
                    fecha_nacimiento=fecha_nacimiento, 
                    email=email, 
                    password=hashed_password,
                    fecha_registro=datetime.datetime.now(LIMA_TZ)
                )
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
        user = Usuario.query.filter_by(email=email).first()
        if user:
            token = user.generate_reset_token()
            
            # Crear el enlace de reseteo
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Enviar email
            try:
                msg = Message(
                    'Recuperar contraseña - AssetNext',
                    recipients=[email]
                )
                
                # Renderizar el template HTML con las variables
                msg.html = render_template('email.html', reset_url=reset_url)
                
                # También incluir versión de texto plano como fallback
                msg.body = f'''Para resetear tu contraseña, haz clic en el siguiente enlace:

{reset_url}

Si no solicitaste este cambio, ignora este mensaje.

El enlace expira en 15 minutos.
'''
                
                mail.send(msg)
                success = 'Se han enviado instrucciones a tu correo.'
            except Exception as e:
                error = 'Error al enviar el correo. Intenta de nuevo.'
        else:
            error = 'El correo no está registrado.'
    return render_template('olvidarcontraseña.html', error=error, success=success)

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = Usuario.query.filter_by(reset_token=token).first()
    
    # Verificar si el token es inválido o ha expirado
    if not user or not user.verify_reset_token(token):
        # Renderizar la misma página pero con token_expired=True
        return render_template('reset_password.html', token_expired=True)
    
    error = None
    success = None
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error = 'Las contraseñas no coinciden.'
        elif len(password) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'
        elif check_password_hash(user.password, password):
            error = 'La nueva contraseña debe ser diferente a la actual.'
        else:
            # Actualizar la contraseña
            user.password = generate_password_hash(password)
            # Limpiar el token para que no se pueda usar de nuevo
            user.clear_reset_token()
            db.session.commit()
            
            success = 'Tu contraseña ha sido actualizada exitosamente.'
    
    return render_template('reset_password.html', error=error, success=success, token_expired=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
from flask import Flask, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Inicialización sin app
db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.secret_key = 'supersecretkey'  # Cambia esto en producción

db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models
from app.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ==============================
# MANEJADORES DE ERRORES - AssetNext
# ==============================

from datetime import datetime

@app.errorhandler(400)  # Solicitud incorrecta
def bad_request(e):
    return render_template("error.html",
        code=400,
        title="Solicitud Incorrecta",
        description="Los datos enviados no son válidos o están mal formateados. Verifica la información e intenta nuevamente.",
        icon="fas fa-exclamation-triangle",
        back_url=url_for('home')
    ), 400

@app.errorhandler(401)  # No autorizado 
def unauthorized(e):
    return render_template("error.html",
        code=401,
        title="Acceso No Autorizado",
        description="Tu sesión ha expirado o no tienes permisos para acceder. Inicia sesión para continuar.",
        icon="fas fa-lock",
        back_url=url_for('home')
    ), 401

@app.errorhandler(403)  # Prohibido
def forbidden(e):
    return render_template("error.html",
        code=403,
        title="Acceso Denegado",
        description="No tienes los permisos necesarios para realizar esta acción o acceder a este recurso.",
        icon="fas fa-ban",
        back_url=url_for('home')
    ), 403

@app.errorhandler(404)  # Página no encontrada
def page_not_found(e):
    return render_template("error.html",
        code=404,
        title="Página No Encontrada",
        description="La página que buscas no existe o ha sido movida. Verifica la URL e intenta nuevamente.",
        icon="fas fa-search",
        back_url=url_for('home')
    ), 404

@app.errorhandler(405)  # Método no permitido
def method_not_allowed(e):
    return render_template("error.html",
        code=405,
        title="Método No Permitido",
        description="El método HTTP utilizado no está permitido para esta ruta. Contacta al administrador si el problema persiste.",
        icon="fas fa-times-circle",
        back_url=url_for('home')
    ), 405

@app.errorhandler(413)  # Archivo demasiado grande
def payload_too_large(e):
    return render_template("error.html",
        code=413,
        title="Archivo Demasiado Grande",
        description="El archivo que intentas subir excede el tamaño máximo permitido. Reduce el tamaño e intenta nuevamente.",
        icon="fas fa-file-upload",
        back_url=url_for('home')
    ), 413

@app.errorhandler(415)  # Tipo de medio no soportado
def unsupported_media_type(e):
    return render_template("error.html",
        code=415,
        title="Tipo de Archivo No Soportado",
        description="El formato del archivo no es compatible. Utiliza un formato válido e intenta nuevamente.",
        icon="fas fa-file-times",
        back_url=url_for('home')
    ), 415

@app.errorhandler(422)  # Entidad no procesable
def unprocessable_entity(e):
    return render_template("error.html",
        code=422,
        title="Datos No Procesables",
        description="Los datos enviados están incompletos o contienen errores. Revisa la información e intenta nuevamente.",
        icon="fas fa-exclamation",
        back_url=url_for('home')
    ), 422

@app.errorhandler(429)  # Demasiadas peticiones
def too_many_requests(e):
    return render_template("error.html",
        code=429,
        title="Demasiadas Peticiones",
        description="Has realizado demasiadas solicitudes en poco tiempo. Espera unos minutos antes de intentar nuevamente.",
        icon="fas fa-hourglass-half",
        back_url=url_for('home')
    ), 429

@app.errorhandler(500)  # Error interno del servidor
def internal_server_error(e):
    # Log del error para debugging
    app.logger.error(f'Error 500: {str(e)}', exc_info=True)
    
    return render_template("error.html",
        code=500,
        title="Error Interno del Sistema",
        description="Ha ocurrido un error inesperado en nuestros servidores. Nuestro equipo técnico ha sido notificado automáticamente.",
        icon="fas fa-server",
        back_url=url_for('home')
    ), 500

@app.errorhandler(502)  # Bad Gateway
def bad_gateway(e):
    return render_template("error.html",
        code=502,
        title="Puerta de Enlace Incorrecta",
        description="Error de comunicación con los servidores. Intenta recargar la página en unos momentos.",
        icon="fas fa-network-wired",
        back_url=url_for('home')
    ), 502

@app.errorhandler(503)  # Servicio no disponible
def service_unavailable(e):
    return render_template("error.html",
        code=503,
        title="Servicio Temporalmente No Disponible",
        description="El sistema está en mantenimiento o experimentando alta demanda. Intenta nuevamente en unos minutos.",
        icon="fas fa-tools",
        back_url=url_for('home')
    ), 503

@app.errorhandler(504)  # Gateway Timeout
def gateway_timeout(e):
    return render_template("error.html",
        code=504,
        title="Tiempo de Espera Excedido",
        description="La operación tardó demasiado en completarse. Intenta nuevamente o contacta al soporte técnico.",
        icon="fas fa-clock",
        back_url=url_for('home')
    ), 504

# ==============================
# MANEJADOR GENÉRICO DE ERRORES
# ==============================

@app.errorhandler(Exception)
def handle_exception(e):
    """Manejador genérico para errores no capturados"""
    
    # Log del error completo
    app.logger.error(f'Error no manejado: {str(e)}', exc_info=True)
    
    # Si es un error HTTP conocido, usar su código
    if hasattr(e, 'code'):
        return render_template("error.html",
            code=e.code,
            title="Error del Sistema",
            description=f"Ha ocurrido un error: {str(e)}",
            icon="fas fa-bolt",
            back_url=url_for('home')
        ), e.code
    
    # Para errores desconocidos, mostrar como error 500
    return render_template("error.html",
        code=500,
        title="Error Inesperado",
        description="Ha ocurrido un error no identificado. Nuestro equipo técnico ha sido notificado.",
        icon="fas fa-times",
        back_url=url_for('home')
    ), 500
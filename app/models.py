from . import db
from flask_login import UserMixin
import secrets
from datetime import datetime, timedelta
import pytz

# Configurar zona horaria de Lima, Perú
LIMA_TZ = pytz.timezone('America/Lima')

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    apellido = db.Column(db.String(64), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(LIMA_TZ))
    reset_token = db.Column(db.String(100), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    ultima_conexion = db.Column(db.DateTime, nullable=True)
    
    def generate_reset_token(self):
        """Genera un token de reseteo que expira en 15 minutos"""
        self.reset_token = secrets.token_urlsafe(32)
        self.token_expiry = datetime.now(LIMA_TZ) + timedelta(minutes=15)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verifica si el token es válido y no ha expirado"""
        if self.reset_token != token:
            return False
            
        # Si no hay token_expiry, el token es inválido
        if not self.token_expiry:
            return False
            
        # Obtener datetime actual
        now = datetime.now(LIMA_TZ)
        
        # Si token_expiry no tiene zona horaria, asumimos que es Lima
        if self.token_expiry.tzinfo is None:
            token_expiry_aware = LIMA_TZ.localize(self.token_expiry)
        else:
            token_expiry_aware = self.token_expiry
            
        # Verificar si el token ha expirado
        if token_expiry_aware > now:
            return True
        else:
            # Token expirado, lo limpiamos automáticamente
            self.clear_reset_token()
            return False
    
    def clear_reset_token(self):
        """Limpia el token después de usarlo o cuando expira"""
        self.reset_token = None
        self.token_expiry = None
        db.session.commit()
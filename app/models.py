from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    sesiones = db.relationship('SesionMusculacion', backref='usuario', lazy=True)
    rutas = db.relationship('Ruta', backref='usuario', lazy=True)

class SesionMusculacion(db.Model):
    __tablename__ = 'sesiones_musculacion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    nombre = db.Column(db.String(100), nullable=False)
    notas = db.Column(db.Text)

    ejercicios = db.relationship('Ejercicio', backref='sesion', lazy=True)

class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'
    id = db.Column(db.Integer, primary_key=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesiones_musculacion.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float)

class Ruta(db.Model):
    __tablename__ = 'rutas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.String(20), nullable=False)
    distancia_km = db.Column(db.Float, nullable=False)
    duracion_min = db.Column(db.Integer, nullable=False)
    notas = db.Column(db.Text)
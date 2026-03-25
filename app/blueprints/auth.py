from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        usuario_existe = Usuario.query.filter_by(email=email).first()
        if usuario_existe:
            flash('Este email ya está registrado.', 'danger')
            return redirect(url_for('auth.registro'))

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Cuenta creada correctamente. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
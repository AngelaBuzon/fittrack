from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import Ruta

rutas_bp = Blueprint('rutas', __name__)

@rutas_bp.route('/')
@login_required
def index():
    rutas = Ruta.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Ruta.fecha.desc()).all()
    return render_template('rutas.html', rutas=rutas)

@rutas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_ruta():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        distancia_km = request.form.get('distancia_km')
        duracion_min = request.form.get('duracion_min')
        notas = request.form.get('notas')

        ruta = Ruta(
            tipo=tipo,
            distancia_km=float(distancia_km),
            duracion_min=int(duracion_min),
            notas=notas,
            usuario_id=current_user.id
        )
        db.session.add(ruta)
        db.session.commit()
        return redirect(url_for('rutas.index'))

    return render_template('nueva_ruta.html')
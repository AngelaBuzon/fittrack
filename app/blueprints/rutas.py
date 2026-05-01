from flask import Blueprint, render_template, redirect, url_for, request, flash
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
        tipo = request.form.get('tipo', '').strip()
        distancia_km = request.form.get('distancia_km', '').strip()
        duracion_min = request.form.get('duracion_min', '').strip()
        notas = request.form.get('notas', '').strip()

        if not tipo:
            flash('Debes seleccionar el tipo de actividad.', 'danger')
            return redirect(url_for('rutas.nueva_ruta'))

        if not distancia_km or float(distancia_km) <= 0:
            flash('La distancia debe ser mayor que 0.', 'danger')
            return redirect(url_for('rutas.nueva_ruta'))

        if not duracion_min or int(duracion_min) <= 0:
            flash('La duración debe ser mayor que 0.', 'danger')
            return redirect(url_for('rutas.nueva_ruta'))

        try:
            ruta = Ruta(
                tipo=tipo,
                distancia_km=float(distancia_km),
                duracion_min=int(duracion_min),
                notas=notas,
                usuario_id=current_user.id
            )
            db.session.add(ruta)
            db.session.commit()
            flash('Ruta guardada correctamente.', 'success')
            return redirect(url_for('rutas.index'))

        except Exception as e:
            db.session.rollback()
            flash('Error al guardar la ruta. Revisa los datos.', 'danger')
            return redirect(url_for('rutas.nueva_ruta'))

    return render_template('nueva_ruta.html')
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import SesionMusculacion, Ejercicio

musculacion_bp = Blueprint('musculacion', __name__)

@musculacion_bp.route('/')
@login_required
def index():
    sesiones = SesionMusculacion.query.filter_by(
        usuario_id=current_user.id
    ).order_by(SesionMusculacion.fecha.desc()).all()
    return render_template('musculacion.html', sesiones=sesiones)

@musculacion_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_sesion():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        notas = request.form.get('notas')

        sesion = SesionMusculacion(
            nombre=nombre,
            notas=notas,
            usuario_id=current_user.id
        )
        db.session.add(sesion)
        db.session.flush()

        ejercicios_nombres = request.form.getlist('ejercicio_nombre')
        series_list = request.form.getlist('series')
        reps_list = request.form.getlist('repeticiones')
        pesos_list = request.form.getlist('peso')

        for i in range(len(ejercicios_nombres)):
            ejercicio = Ejercicio(
                sesion_id=sesion.id,
                nombre=ejercicios_nombres[i],
                series=int(series_list[i]),
                repeticiones=int(reps_list[i]),
                peso=float(pesos_list[i]) if pesos_list[i] else None
            )
            db.session.add(ejercicio)

        db.session.commit()
        return redirect(url_for('musculacion.index'))

    return render_template('nueva_sesion.html')
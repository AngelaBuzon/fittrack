from flask import Blueprint, render_template, redirect, url_for, request, flash
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
        nombre = request.form.get('nombre', '').strip()
        notas = request.form.get('notas', '').strip()

        if not nombre:
            flash('El nombre de la sesión es obligatorio.', 'danger')
            return redirect(url_for('musculacion.nueva_sesion'))

        ejercicios_nombres = request.form.getlist('ejercicio_nombre')
        series_list = request.form.getlist('series')
        reps_list = request.form.getlist('repeticiones')
        pesos_list = request.form.getlist('peso')

        if not ejercicios_nombres or not ejercicios_nombres[0].strip():
            flash('Debes añadir al menos un ejercicio.', 'danger')
            return redirect(url_for('musculacion.nueva_sesion'))

        try:
            sesion = SesionMusculacion(
                nombre=nombre,
                notas=notas,
                usuario_id=current_user.id
            )
            db.session.add(sesion)
            db.session.flush()

            for i in range(len(ejercicios_nombres)):
                if not ejercicios_nombres[i].strip():
                    continue
                ejercicio = Ejercicio(
                    sesion_id=sesion.id,
                    nombre=ejercicios_nombres[i].strip(),
                    series=int(series_list[i]),
                    repeticiones=int(reps_list[i]),
                    peso=float(pesos_list[i]) if pesos_list[i] else None
                )
                db.session.add(ejercicio)

            db.session.commit()
            flash('Sesión guardada correctamente.', 'success')
            return redirect(url_for('musculacion.index'))

        except Exception as e:
            db.session.rollback()
            flash('Error al guardar la sesión. Revisa los datos.', 'danger')
            return redirect(url_for('musculacion.nueva_sesion'))

    return render_template('nueva_sesion.html')
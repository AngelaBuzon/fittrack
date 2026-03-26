from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import SesionMusculacion, Ruta, Ejercicio
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    sesiones = SesionMusculacion.query.filter_by(
        usuario_id=current_user.id
    ).order_by(SesionMusculacion.fecha.asc()).all()

    rutas = Ruta.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Ruta.fecha.asc()).all()

    sesiones_fechas = [s.fecha.strftime('%d/%m') for s in sesiones]
    sesiones_count = list(range(1, len(sesiones) + 1))

    rutas_fechas = [r.fecha.strftime('%d/%m') for r in rutas]
    rutas_distancias = [r.distancia_km for r in rutas]

    total_sesiones = len(sesiones)
    total_rutas = len(rutas)
    total_km = round(sum(r.distancia_km for r in rutas), 1)
    total_minutos = sum(r.duracion_min for r in rutas)

    mejor_ruta = max(rutas, key=lambda r: r.distancia_km) if rutas else None

    ejercicios = Ejercicio.query.join(SesionMusculacion).filter(
        SesionMusculacion.usuario_id == current_user.id
    ).all()
    peso_maximo = max((e.peso for e in ejercicios if e.peso), default=0)

    return render_template('dashboard.html',
        sesiones_fechas=sesiones_fechas,
        sesiones_count=sesiones_count,
        rutas_fechas=rutas_fechas,
        rutas_distancias=rutas_distancias,
        total_sesiones=total_sesiones,
        total_rutas=total_rutas,
        total_km=total_km,
        total_minutos=total_minutos,
        mejor_ruta=mejor_ruta,
        peso_maximo=peso_maximo
    )

@dashboard_bp.route('/historial')
@login_required
def historial():
    tipo = request.args.get('tipo', '')
    fecha_desde = request.args.get('fecha_desde', '')
    fecha_hasta = request.args.get('fecha_hasta', '')

    actividades = []

    if tipo == '' or tipo == 'musculacion':
        sesiones = SesionMusculacion.query.filter_by(usuario_id=current_user.id)
        if fecha_desde:
            sesiones = sesiones.filter(SesionMusculacion.fecha >= datetime.strptime(fecha_desde, '%Y-%m-%d'))
        if fecha_hasta:
            sesiones = sesiones.filter(SesionMusculacion.fecha <= datetime.strptime(fecha_hasta, '%Y-%m-%d'))
        for s in sesiones.all():
            actividades.append({
                'tipo': 'musculacion',
                'fecha': s.fecha,
                'nombre': s.nombre,
                'detalle': s.notas
            })

    if tipo == '' or tipo == 'running' or tipo == 'ciclismo':
        rutas = Ruta.query.filter_by(usuario_id=current_user.id)
        if tipo in ['running', 'ciclismo']:
            rutas = rutas.filter_by(tipo=tipo)
        if fecha_desde:
            rutas = rutas.filter(Ruta.fecha >= datetime.strptime(fecha_desde, '%Y-%m-%d'))
        if fecha_hasta:
            rutas = rutas.filter(Ruta.fecha <= datetime.strptime(fecha_hasta, '%Y-%m-%d'))
        for r in rutas.all():
            actividades.append({
                'tipo': r.tipo,
                'fecha': r.fecha,
                'nombre': f'{r.distancia_km} km en {r.duracion_min} min',
                'detalle': r.notas
            })

    actividades.sort(key=lambda x: x['fecha'], reverse=True)

    return render_template('historial.html',
        actividades=actividades,
        tipo=tipo,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
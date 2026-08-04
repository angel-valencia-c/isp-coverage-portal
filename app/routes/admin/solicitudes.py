"""
Blueprint de Gestión de Solicitudes

Rutas para el panel administrativo de gestión de solicitudes.
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, Response
from flask_login import login_required, current_user
from app.services.gestion_solicitudes_service import GestionSolicitudesService
from app.services.auth_service import AuthService

solicitudes_bp = Blueprint('solicitudes', __name__, url_prefix='/admin/solicitudes')


@solicitudes_bp.route('/')
@login_required
@AuthService.require_admin
def listar_solicitudes():
    """
    Lista todas las solicitudes con filtros opcionales.
    """
    # Obtener filtros
    estado = request.args.get('estado')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    ordenar_por = request.args.get('ordenar_por', 'fecha_creacion')
    orden = request.args.get('orden', 'desc')
    
    # Convertir fechas
    from datetime import datetime
    fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d') if fecha_desde else None
    fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d') if fecha_hasta else None
    
    # Obtener solicitudes
    solicitudes = GestionSolicitudesService.get_solicitudes(
        estado=estado,
        fecha_desde=fecha_desde_dt,
        fecha_hasta=fecha_hasta_dt,
        ordenar_por=ordenar_por,
        orden=orden
    )
    
    # Obtener estadísticas
    estadisticas = GestionSolicitudesService.get_estadisticas()
    
    return render_template(
        'pages/admin/solicitudes/list.html',
        solicitudes=solicitudes,
        estadisticas=estadisticas,
        filtros={
            'estado': estado,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'ordenar_por': ordenar_por,
            'orden': orden
        }
    )


@solicitudes_bp.route('/<int:solicitud_id>')
@login_required
@AuthService.require_admin
def detalle_solicitud(solicitud_id):
    """
    Muestra el detalle de una solicitud.
    """
    solicitud = GestionSolicitudesService.get_solicitud_by_id(solicitud_id)
    
    if not solicitud:
        flash('Solicitud no encontrada', 'error')
        return redirect(url_for('solicitudes.listar_solicitudes'))
    
    return render_template(
        'pages/admin/solicitudes/detalle.html',
        solicitud=solicitud
    )


@solicitudes_bp.route('/<int:solicitud_id>/cambiar-estado', methods=['POST'])
@login_required
@AuthService.require_admin
def cambiar_estado(solicitud_id):
    """
    Cambia el estado de una solicitud.
    """
    nuevo_estado = request.form.get('estado')
    
    try:
        GestionSolicitudesService.cambiar_estado(
            solicitud_id=solicitud_id,
            nuevo_estado=nuevo_estado,
            usuario_id=current_user.id
        )
        flash('Estado actualizado correctamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('solicitudes.detalle_solicitud', solicitud_id=solicitud_id))


@solicitudes_bp.route('/<int:solicitud_id>/marcar-duplicada', methods=['POST'])
@login_required
@AuthService.require_admin
def marcar_duplicada(solicitud_id):
    """
    Marca una solicitud como duplicada.
    """
    solicitud_original_id = request.form.get('solicitud_original_id', type=int)
    
    try:
        GestionSolicitudesService.marcar_como_duplicada(
            solicitud_id=solicitud_id,
            solicitud_original_id=solicitud_original_id,
            usuario_id=current_user.id
        )
        flash('Solicitud marcada como duplicada', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('solicitudes.detalle_solicitud', solicitud_id=solicitud_id))


@solicitudes_bp.route('/exportar')
@login_required
@AuthService.require_admin
def exportar_csv():
    """
    Exporta solicitudes a CSV con filtros opcionales.
    """
    # Obtener filtros
    estado = request.args.get('estado')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    # Convertir fechas
    from datetime import datetime
    fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d') if fecha_desde else None
    fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d') if fecha_hasta else None
    
    # Obtener solicitudes
    solicitudes = GestionSolicitudesService.get_solicitudes(
        estado=estado,
        fecha_desde=fecha_desde_dt,
        fecha_hasta=fecha_hasta_dt
    )
    
    # Exportar a CSV
    csv_content = GestionSolicitudesService.exportar_a_csv(solicitudes)
    
    # Crear respuesta
    output = Response(
        csv_content,
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=solicitudes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )
    
    return output

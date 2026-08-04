"""
Blueprint de Análisis de Demanda

Rutas para el panel administrativo de análisis de demanda por zona.
"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.services.analisis_demanda_service import AnalisisDemandaService
from app.services.auth_service import AuthService
from app.services.gestion_solicitudes_service import GestionSolicitudesService
from datetime import datetime

analisis_bp = Blueprint('analisis', __name__, url_prefix='/admin/analisis')


@analisis_bp.route('/demanda')
@login_required
@AuthService.require_admin
def demanda():
    """
    Página de análisis de demanda por zona.
    """
    # Obtener filtros
    fecha_desde_str = request.args.get('fecha_desde')
    fecha_hasta_str = request.args.get('fecha_hasta')
    estado = request.args.get('estado')
    municipio_id = request.args.get('municipio_id', type=int)
    
    # Convertir fechas
    fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d') if fecha_desde_str else None
    fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d') if fecha_hasta_str else None
    
    # Obtener datos de análisis
    demand_municipio = AnalisisDemandaService.get_demand_por_municipio(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado=estado
    )
    
    demand_colonia = AnalisisDemandaService.get_demand_por_colonia(
        municipio_id=municipio_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado=estado
    )
    
    demand_cobertura = AnalisisDemandaService.get_demand_con_vs_sin_cobertura(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado=estado
    )
    
    top_colonias = AnalisisDemandaService.get_top_colonias(
        limit=10,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        estado=estado
    )
    
    demand_estado = AnalisisDemandaService.get_demand_por_estado(
        municipio_id=municipio_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    # Obtener municipios para filtro
    from app.services.municipio_service import MunicipioService
    municipios = MunicipioService.get_all()
    
    # Obtener estadísticas generales
    estadisticas = GestionSolicitudesService.get_estadisticas()
    
    return render_template(
        'pages/admin/analisis/demanda.html',
        demand_municipio=demand_municipio,
        demand_colonia=demand_colonia,
        demand_cobertura=demand_cobertura,
        top_colonias=top_colonias,
        demand_estado=demand_estado,
        municipios=municipios,
        estadisticas=estadisticas,
        filtros={
            'fecha_desde': fecha_desde_str,
            'fecha_hasta': fecha_hasta_str,
            'estado': estado,
            'municipio_id': municipio_id
        }
    )

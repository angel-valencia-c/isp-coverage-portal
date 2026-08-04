"""
Blueprint de Administración

Rutas del panel administrativo.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.dashboard_service import DashboardService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard principal del panel administrativo.
    """
    metricas = DashboardService.get_metricas_generales()
    solicitudes_recientes = DashboardService.get_solicitudes_recientes(limit=10)
    resumen_estado = DashboardService.get_resumen_por_estado()
    
    return render_template(
        'pages/admin/dashboard.html',
        usuario=current_user,
        metricas=metricas,
        solicitudes_recientes=solicitudes_recientes,
        resumen_estado=resumen_estado
    )


@admin_bp.route('/territorio')
@login_required
def territorio():
    """
    Vista jerárquica del territorio.
    """
    from flask import request
    municipio_id = request.args.get('municipio_id', type=int)
    
    vista_jerarquica = DashboardService.get_vista_jerarquica(municipio_id=municipio_id)
    
    # Obtener municipios para el filtro
    from app.models.municipio import Municipio
    municipios = Municipio.query.filter_by(activo=True).order_by(Municipio.nombre).all()
    
    return render_template(
        'pages/admin/territorio.html',
        vista_jerarquica=vista_jerarquica,
        municipios=municipios,
        municipio_id=municipio_id
    )

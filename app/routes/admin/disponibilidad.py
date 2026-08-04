"""
Blueprint de Disponibilidad de Planes

Rutas para gestión de asociación de planes a zonas de cobertura.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.disponibilidad_plan_service import DisponibilidadPlanService
from app.services.cobertura_service import CoberturaService
from app.services.auth_service import AuthService

disponibilidad_bp = Blueprint('disponibilidad', __name__, url_prefix='/admin/disponibilidad')


@disponibilidad_bp.route('/cobertura/<int:cobertura_id>')
@login_required
def list_by_cobertura(cobertura_id):
    """
    Lista los planes disponibles en una cobertura específica.
    """
    cobertura = CoberturaService.get_by_id(cobertura_id)
    if not cobertura:
        flash('Cobertura no encontrada', 'error')
        return redirect(url_for('cobertura.list'))
    
    disponibilidades = DisponibilidadPlanService.get_by_cobertura(cobertura_id)
    planes_disponibles = DisponibilidadPlanService.get_planes_disponibles_para_asociar(cobertura_id)
    
    return render_template(
        'pages/admin/disponibilidad/list.html',
        cobertura=cobertura,
        disponibilidades=disponibilidades,
        planes_disponibles=planes_disponibles
    )


@disponibilidad_bp.route('/cobertura/<int:cobertura_id>/add', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def add_plan(cobertura_id):
    """
    Asocia un plan a una cobertura.
    """
    plan_id = request.form.get('plan_id', type=int)
    costo_instalacion = request.form.get('costo_instalacion', type=float)
    
    try:
        DisponibilidadPlanService.create(
            cobertura_id=cobertura_id,
            plan_id=plan_id,
            costo_instalacion=costo_instalacion,
            usuario_id=current_user.id
        )
        flash('Plan asociado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('disponibilidad.list_by_cobertura', cobertura_id=cobertura_id))


@disponibilidad_bp.route('/<int:disponibilidad_id>/update_costo', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def update_costo(disponibilidad_id):
    """
    Actualiza el costo de instalación de una disponibilidad.
    """
    costo_instalacion = request.form.get('costo_instalacion', type=float)
    
    try:
        disponibilidad = DisponibilidadPlanService.update_costo(
            disponibilidad_id=disponibilidad_id,
            costo_instalacion=costo_instalacion,
            usuario_id=current_user.id
        )
        flash('Costo actualizado exitosamente', 'success')
        cobertura_id = disponibilidad.cobertura_id
    except ValueError as e:
        flash(str(e), 'error')
        cobertura_id = request.form.get('cobertura_id', type=int)
    
    return redirect(url_for('disponibilidad.list_by_cobertura', cobertura_id=cobertura_id))


@disponibilidad_bp.route('/<int:disponibilidad_id>/remove', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def remove_plan(disponibilidad_id):
    """
    Elimina una asociación plan-cobertura.
    """
    cobertura_id = request.form.get('cobertura_id', type=int)
    
    try:
        DisponibilidadPlanService.remove(
            disponibilidad_id=disponibilidad_id,
            usuario_id=current_user.id
        )
        flash('Plan desasociado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('disponibilidad.list_by_cobertura', cobertura_id=cobertura_id))


@disponibilidad_bp.route('/config/costo-base', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def config_costo_base():
    """
    Configura el costo estándar base de instalación.
    """
    if request.method == 'POST':
        costo_base = request.form.get('costo_base', type=float)
        
        try:
            DisponibilidadPlanService.set_costo_estandar_base(
                costo=costo_base,
                usuario_id=current_user.id
            )
            flash('Costo estándar base configurado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al configurar costo base: {str(e)}', 'error')
        
        return redirect(url_for('disponibilidad.config_costo_base'))
    
    # GET: Mostrar formulario
    costo_base = DisponibilidadPlanService.get_costo_estandar_base()
    return render_template(
        'pages/admin/disponibilidad/config_costo_base.html',
        costo_base=costo_base
    )

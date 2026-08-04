"""
Blueprint de Planes

Rutas para gestión de planes de internet.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.plan_service import PlanService
from app.services.auth_service import AuthService

planes_bp = Blueprint('planes', __name__, url_prefix='/admin/planes')


@planes_bp.route('/')
@login_required
def list():
    """
    Lista todos los planes.
    
    Query params:
        incluir_inactivos: Si 'true', muestra también planes inactivos
    """
    incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
    planes = PlanService.get_all(incluir_inactivos=incluir_inactivos)
    
    return render_template(
        'pages/admin/planes/list.html',
        planes=planes,
        incluir_inactivos=incluir_inactivos
    )


@planes_bp.route('/new', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def new():
    """
    Crea un nuevo plan.
    """
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            velocidad_descarga = int(request.form.get('velocidad_descarga', 0))
            velocidad_subida = int(request.form.get('velocidad_subida', 0))
            precio_mensual = float(request.form.get('precio_mensual', 0))
            descripcion = request.form.get('descripcion', '').strip()
            orden = int(request.form.get('orden', 0))
            destacado = request.form.get('destacado') == 'on'
            
            plan = PlanService.create(
                nombre=nombre,
                velocidad_descarga=velocidad_descarga,
                velocidad_subida=velocidad_subida,
                precio_mensual=precio_mensual,
                descripcion=descripcion if descripcion else None,
                orden=orden,
                destacado=destacado,
                usuario_id=current_user.id
            )
            
            flash(f'Plan "{plan.nombre}" creado exitosamente', 'success')
            return redirect(url_for('planes.list'))
            
        except ValueError as e:
            flash(str(e), 'error')
        except (ValueError, TypeError) as e:
            flash('Error en los datos del formulario', 'error')
    
    return render_template('pages/admin/planes/form.html', plan=None)


@planes_bp.route('/<int:plan_id>/edit', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def edit(plan_id):
    """
    Edita un plan existente.
    """
    plan = PlanService.get_by_id(plan_id)
    if not plan:
        flash('Plan no encontrado', 'error')
        return redirect(url_for('planes.list'))
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            velocidad_descarga = int(request.form.get('velocidad_descarga', 0))
            velocidad_subida = int(request.form.get('velocidad_subida', 0))
            precio_mensual = float(request.form.get('precio_mensual', 0))
            descripcion = request.form.get('descripcion', '').strip()
            orden = int(request.form.get('orden', 0))
            destacado = request.form.get('destacado') == 'on'
            
            plan = PlanService.update(
                plan_id=plan_id,
                nombre=nombre,
                velocidad_descarga=velocidad_descarga,
                velocidad_subida=velocidad_subida,
                precio_mensual=precio_mensual,
                descripcion=descripcion if descripcion else None,
                orden=orden,
                destacado=destacado,
                usuario_id=current_user.id
            )
            
            flash(f'Plan "{plan.nombre}" actualizado exitosamente', 'success')
            return redirect(url_for('planes.list'))
            
        except ValueError as e:
            flash(str(e), 'error')
        except (ValueError, TypeError) as e:
            flash('Error en los datos del formulario', 'error')
    
    return render_template('pages/admin/planes/form.html', plan=plan)


@planes_bp.route('/<int:plan_id>/deactivate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def deactivate(plan_id):
    """
    Desactiva un plan.
    """
    try:
        plan = PlanService.deactivate(plan_id, usuario_id=current_user.id)
        flash(f'Plan "{plan.nombre}" desactivado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('planes.list'))


@planes_bp.route('/<int:plan_id>/activate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def activate(plan_id):
    """
    Activa un plan previamente desactivado.
    """
    try:
        plan = PlanService.activate(plan_id, usuario_id=current_user.id)
        flash(f'Plan "{plan.nombre}" activado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('planes.list'))

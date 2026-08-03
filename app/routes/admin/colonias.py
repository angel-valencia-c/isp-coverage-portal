"""
Blueprint de Administración de Colonias

Rutas para CRUD de colonias/comunidades.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.colonia_service import ColoniaService
from app.services.municipio_service import MunicipioService
from app.services.auth_service import AuthService

colonias_bp = Blueprint('colonias', __name__, url_prefix='/admin/colonias')


@colonias_bp.route('/')
@login_required
def list():
    """
    Lista todas las colonias, opcionalmente filtradas por municipio.
    """
    municipio_id = request.args.get('municipio_id', type=int)
    incluir_inactivos = request.args.get('incluir_inactivos', 'false') == 'true'
    
    colonias = ColoniaService.get_all(
        incluir_inactivos=incluir_inactivos,
        municipio_id=municipio_id
    )
    municipios = MunicipioService.get_all()
    
    return render_template(
        'pages/admin/colonias/list.html',
        colonias=colonias,
        municipios=municipios,
        municipio_id=municipio_id,
        incluir_inactivos=incluir_inactivos
    )


@colonias_bp.route('/new', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def new():
    """
    Crea una nueva colonia/comunidad.
    """
    municipios = MunicipioService.get_all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        tipo = request.form.get('tipo', 'colonia').strip()
        municipio_id = request.form.get('municipio_id', type=int)
        
        if not nombre:
            flash('El nombre de la colonia es obligatorio', 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=None,
                municipios=municipios
            )
        
        if not municipio_id:
            flash('Debes seleccionar un municipio', 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=None,
                municipios=municipios
            )
        
        try:
            colonia = ColoniaService.create(
                nombre=nombre,
                tipo=tipo,
                municipio_id=municipio_id,
                usuario_id=current_user.id
            )
            flash(f'Colonia "{colonia.nombre}" creada exitosamente', 'success')
            return redirect(url_for('colonias.list'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=None,
                municipios=municipios
            )
    
    return render_template(
        'pages/admin/colonias/form.html',
        colonia=None,
        municipios=municipios
    )


@colonias_bp.route('/<int:colonia_id>/edit', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def edit(colonia_id):
    """
    Edita una colonia existente.
    """
    colonia = ColoniaService.get_by_id(colonia_id)
    if not colonia:
        flash('Colonia no encontrada', 'error')
        return redirect(url_for('colonias.list'))
    
    municipios = MunicipioService.get_all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        tipo = request.form.get('tipo', 'colonia').strip()
        municipio_id = request.form.get('municipio_id', type=int)
        
        if not nombre:
            flash('El nombre de la colonia es obligatorio', 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=colonia,
                municipios=municipios
            )
        
        if not municipio_id:
            flash('Debes seleccionar un municipio', 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=colonia,
                municipios=municipios
            )
        
        try:
            colonia = ColoniaService.update(
                colonia_id=colonia_id,
                nombre=nombre,
                tipo=tipo,
                municipio_id=municipio_id,
                usuario_id=current_user.id
            )
            flash(f'Colonia "{colonia.nombre}" actualizada exitosamente', 'success')
            return redirect(url_for('colonias.list'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template(
                'pages/admin/colonias/form.html',
                colonia=colonia,
                municipios=municipios
            )
    
    return render_template(
        'pages/admin/colonias/form.html',
        colonia=colonia,
        municipios=municipios
    )


@colonias_bp.route('/<int:colonia_id>/deactivate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def deactivate(colonia_id):
    """
    Desactiva una colonia.
    """
    try:
        colonia = ColoniaService.deactivate(
            colonia_id=colonia_id,
            usuario_id=current_user.id
        )
        flash(f'Colonia "{colonia.nombre}" desactivada exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('colonias.list'))


@colonias_bp.route('/<int:colonia_id>/activate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def activate(colonia_id):
    """
    Activa una colonia previamente desactivada.
    """
    try:
        colonia = ColoniaService.activate(
            colonia_id=colonia_id,
            usuario_id=current_user.id
        )
        flash(f'Colonia "{colonia.nombre}" activada exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('colonias.list'))

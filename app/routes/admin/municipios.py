"""
Blueprint de Administración de Municipios

Rutas para CRUD de municipios.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.municipio_service import MunicipioService
from app.services.auth_service import AuthService

municipios_bp = Blueprint('municipios', __name__, url_prefix='/admin/municipios')


@municipios_bp.route('/')
@login_required
def list():
    """
    Lista todos los municipios.
    """
    incluir_inactivos = request.args.get('incluir_inactivos', 'false') == 'true'
    municipios = MunicipioService.get_all(incluir_inactivos=incluir_inactivos)
    return render_template(
        'pages/admin/municipios/list.html',
        municipios=municipios,
        incluir_inactivos=incluir_inactivos
    )


@municipios_bp.route('/new', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def new():
    """
    Crea un nuevo municipio.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado', 'Guerrero').strip()
        
        if not nombre:
            flash('El nombre del municipio es obligatorio', 'error')
            return render_template('pages/admin/municipios/form.html', municipio=None)
        
        try:
            municipio = MunicipioService.create(
                nombre=nombre,
                estado=estado,
                usuario_id=current_user.id
            )
            flash(f'Municipio "{municipio.nombre}" creado exitosamente', 'success')
            return redirect(url_for('municipios.list'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('pages/admin/municipios/form.html', municipio=None)
    
    return render_template('pages/admin/municipios/form.html', municipio=None)


@municipios_bp.route('/<int:municipio_id>/edit', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def edit(municipio_id):
    """
    Edita un municipio existente.
    """
    municipio = MunicipioService.get_by_id(municipio_id)
    if not municipio:
        flash('Municipio no encontrado', 'error')
        return redirect(url_for('municipios.list'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado', 'Guerrero').strip()
        
        if not nombre:
            flash('El nombre del municipio es obligatorio', 'error')
            return render_template('pages/admin/municipios/form.html', municipio=municipio)
        
        try:
            municipio = MunicipioService.update(
                municipio_id=municipio_id,
                nombre=nombre,
                estado=estado,
                usuario_id=current_user.id
            )
            flash(f'Municipio "{municipio.nombre}" actualizado exitosamente', 'success')
            return redirect(url_for('municipios.list'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('pages/admin/municipios/form.html', municipio=municipio)
    
    return render_template('pages/admin/municipios/form.html', municipio=municipio)


@municipios_bp.route('/<int:municipio_id>/deactivate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def deactivate(municipio_id):
    """
    Desactiva un municipio.
    """
    try:
        municipio = MunicipioService.deactivate(
            municipio_id=municipio_id,
            usuario_id=current_user.id
        )
        flash(f'Municipio "{municipio.nombre}" desactivado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('municipios.list'))


@municipios_bp.route('/<int:municipio_id>/activate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def activate(municipio_id):
    """
    Activa un municipio previamente desactivado.
    """
    try:
        municipio = MunicipioService.activate(
            municipio_id=municipio_id,
            usuario_id=current_user.id
        )
        flash(f'Municipio "{municipio.nombre}" activado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('municipios.list'))

"""
Blueprint de Colonias

Rutas CRUD para gestión de colonias/comunidades.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import require_auth, require_role, get_current_user
from app.services.colonia_service import ColoniaService
from app.services.municipio_service import MunicipioService

colonias_bp = Blueprint('colonias', __name__, url_prefix='/admin/colonias')


@colonias_bp.route('/')
@require_auth
@require_role('superadministrador', 'administrador')
def list():
    """ 
    Lista todas las colonias, opcionalmente filtradas por municipio.
    """
    municipio_id = request.args.get('municipio_id', type=int)
    colonias = ColoniaService.get_all_colonias(municipio_id)
    municipios = MunicipioService.get_all_municipios()
    stats = ColoniaService.get_colonias_stats(municipio_id)
    
    return render_template('admin/colonias/list.html', 
                         colonias=colonias,
                         municipios=municipios,
                         municipio_id=municipio_id,
                         stats=stats)


@colonias_bp.route('/create', methods=['GET', 'POST'])
@require_auth
@require_role('superadministrador')
def create():
    """
    Crea una nueva colonia.
    """
    municipios = MunicipioService.get_all_municipios()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        municipio_id = request.form.get('municipio_id', type=int)
        activo = request.form.get('activo') == 'on'
        
        usuario = get_current_user()
        colonia, error = ColoniaService.create_colonia(
            nombre=nombre,
            tipo=tipo,
            municipio_id=municipio_id,
            activo=activo,
            creado_por=usuario.id
        )
        
        if error:
            flash(error, 'error')
            return render_template('admin/colonias/form.html', 
                                 colonia=None, 
                                 municipios=municipios,
                                 action='create')
        
        flash(f'Colonia "{nombre}" creada exitosamente', 'success')
        return redirect(url_for('colonias.list'))
    
    return render_template('admin/colonias/form.html', 
                         colonia=None, 
                         municipios=municipios,
                         action='create')


@colonias_bp.route('/<int:colonia_id>/edit', methods=['GET', 'POST'])
@require_auth
@require_role('superadministrador')
def edit(colonia_id):
    """
    Edita una colonia existente.
    """
    colonia = ColoniaService.get_colonia_by_id(colonia_id)
    if not colonia:
        flash('Colonia no encontrada', 'error')
        return redirect(url_for('colonias.list'))
    
    municipios = MunicipioService.get_all_municipios()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        municipio_id = request.form.get('municipio_id', type=int)
        activo = request.form.get('activo') == 'on'
        
        usuario = get_current_user()
        colonia, error = ColoniaService.update_colonia(
            colonia_id=colonia_id,
            nombre=nombre,
            tipo=tipo,
            municipio_id=municipio_id,
            activo=activo,
            actualizado_por=usuario.id
        )
        
        if error:
            flash(error, 'error')
            return render_template('admin/colonias/form.html', 
                                 colonia=colonia, 
                                 municipios=municipios,
                                 action='edit')
        
        flash(f'Colonia "{nombre}" actualizada exitosamente', 'success')
        return redirect(url_for('colonias.list'))
    
    return render_template('admin/colonias/form.html', 
                         colonia=colonia, 
                         municipios=municipios,
                         action='edit')


@colonias_bp.route('/<int:colonia_id>/delete', methods=['POST'])
@require_auth
@require_role('superadministrador')
def delete(colonia_id):
    """
    Elimina una colonia.
    """
    exito, error = ColoniaService.delete_colonia(colonia_id)
    
    if error:
        flash(error, 'error')
    else:
        flash('Colonia eliminada exitosamente', 'success')
    
    return redirect(url_for('colonias.list'))


@colonias_bp.route('/<int:colonia_id>/toggle', methods=['POST'])
@require_auth
@require_role('superadministrador')
def toggle_activo(colonia_id):
    """
    Activa/desactiva una colonia.
    """
    colonia = ColoniaService.get_colonia_by_id(colonia_id)
    if not colonia:
        flash('Colonia no encontrada', 'error')
        return redirect(url_for('colonias.list'))
    
    usuario = get_current_user()
    nuevo_estado = not colonia.activo
    
    colonia, error = ColoniaService.update_colonia(
        colonia_id=colonia_id,
        activo=nuevo_estado,
        actualizado_por=usuario.id
    )
    
    if error:
        flash(error, 'error')
    else:
        estado_texto = 'activada' if nuevo_estado else 'desactivada'
        flash(f'Colonia {estado_texto} exitosamente', 'success')
    
    return redirect(url_for('colonias.list'))

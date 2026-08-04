"""
Blueprint de Administración de Cobertura

Rutas para gestión de cobertura por colonia.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.cobertura_service import CoberturaService
from app.services.colonia_service import ColoniaService
from app.services.municipio_service import MunicipioService
from app.services.auth_service import AuthService

cobertura_bp = Blueprint('cobertura', __name__, url_prefix='/admin/cobertura')


@cobertura_bp.route('/')
@login_required
def list():
    """
    Lista todas las coberturas.
    """
    municipio_id = request.args.get('municipio_id', type=int)
    incluir_inactivas = request.args.get('incluir_inactivas', 'false') == 'true'
    
    coberturas_info = CoberturaService.get_coberturas_con_info(
        incluir_inactivas=incluir_inactivas,
        municipio_id=municipio_id
    )
    municipios = MunicipioService.get_all()
    
    return render_template(
        'pages/admin/cobertura/list.html',
        coberturas_info=coberturas_info,
        municipios=municipios,
        municipio_id=municipio_id,
        incluir_inactivas=incluir_inactivas
    )


@cobertura_bp.route('/colonias/<int:colonia_id>/activate', methods=['GET', 'POST'])
@login_required
@AuthService.require_superadministrador
def activate(colonia_id):
    """
    Activa cobertura en una colonia.
    """
    if request.method == 'POST':
        tipo_cobertura = request.form.get('tipo_cobertura', 'total')
        notas = request.form.get('notas', '').strip()
        
        try:
            cobertura = CoberturaService.activate(
                colonia_id=colonia_id,
                tipo_cobertura=tipo_cobertura,
                notas=notas if notas else None,
                usuario_id=current_user.id
            )
            flash(f'Cobertura activada exitosamente para la colonia', 'success')
            return redirect(url_for('cobertura.list'))
        except ValueError as e:
            flash(str(e), 'error')
    
    # GET: Mostrar formulario de activación
    from app.models.colonia import ColoniaComunidad
    colonia = ColoniaComunidad.query.get(colonia_id)
    if not colonia:
        flash('Colonia no encontrada', 'error')
        return redirect(url_for('cobertura.list'))
    
    return render_template(
        'pages/admin/cobertura/activate.html',
        colonia=colonia
    )


@cobertura_bp.route('/colonias/<int:colonia_id>/deactivate', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def deactivate(colonia_id):
    """
    Desactiva cobertura en una colonia.
    """
    forzar = request.form.get('forzar') == 'true'
    
    try:
        cobertura, info_solicitudes = CoberturaService.deactivate(
            colonia_id=colonia_id,
            usuario_id=current_user.id,
            forzar=forzar
        )
        
        # Si hay solicitudes pendientes y no se forzó, mostrar confirmación
        if info_solicitudes['requiere_confirmacion']:
            flash(
                f'Esta colonia tiene {info_solicitudes["cantidad"]} solicitud(es) pendiente(s). '
                f'¿Deseas desactivar la cobertura de todos modos?',
                'warning'
            )
            # Guardar info en sesión para mostrar modal de confirmación
            return render_template(
                'pages/admin/cobertura/confirm_deactivate.html',
                colonia_id=colonia_id,
                solicitudes_pendientes=info_solicitudes['cantidad']
            )
        
        if cobertura:
            flash('Cobertura desactivada exitosamente', 'success')
        return redirect(url_for('cobertura.list'))
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('cobertura.list'))


@cobertura_bp.route('/colonias/<int:colonia_id>/notas', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def update_notas(colonia_id):
    """
    Actualiza las notas de una cobertura.
    """
    notas = request.form.get('notas', '').strip()
    
    try:
        CoberturaService.update_notas(
            colonia_id=colonia_id,
            notas=notas if notas else None,
            usuario_id=current_user.id
        )
        flash('Notas actualizadas exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('cobertura.list'))


@cobertura_bp.route('/colonias/<int:colonia_id>/tipo', methods=['POST'])
@login_required
@AuthService.require_superadministrador
def update_tipo(colonia_id):
    """
    Actualiza el tipo de cobertura.
    """
    tipo_cobertura = request.form.get('tipo_cobertura', 'total')
    
    try:
        CoberturaService.update_tipo(
            colonia_id=colonia_id,
            tipo_cobertura=tipo_cobertura,
            usuario_id=current_user.id
        )
        flash('Tipo de cobertura actualizado exitosamente', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('cobertura.list'))

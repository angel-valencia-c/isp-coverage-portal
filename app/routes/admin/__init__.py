"""
Blueprint de Administración

Rutas del panel administrativo.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard principal del panel administrativo.
    """
    return render_template('pages/admin/dashboard.html', usuario=current_user)

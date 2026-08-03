"""
Blueprint de Autenticación

Rutas para login/logout de usuarios administrativos.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de login y procesamiento de credenciales.
    
    GET: Muestra el formulario de login
    POST: Procesa las credenciales enviadas
    """
    # Si ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validar campos obligatorios
        if not email or not password:
            flash('Por favor ingresa tu email y contraseña', 'error')
            return render_template('pages/admin/login.html', email=email)
        
        # Autenticar usuario
        usuario = AuthService.authenticate(email, password)
        
        if not usuario:
            flash('Credenciales inválidas o usuario inactivo', 'error')
            return render_template('pages/admin/login.html', email=email)
        
        # Iniciar sesión
        if AuthService.login(usuario):
            flash(f'Bienvenido, {usuario.nombre}', 'success')
            # Redirigir a la página solicitada o al dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Error al iniciar sesión', 'error')
            return render_template('pages/admin/login.html', email=email)
    
    # GET: Mostrar formulario de login
    return render_template('pages/admin/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Cierra la sesión del usuario actual.
    """
    AuthService.logout()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))

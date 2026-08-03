"""
Servicio de Autenticación

Maneja la lógica de autenticación de usuarios administrativos:
- Login con email y password
- Logout
- Validación de credenciales
- Gestión de sesiones
"""
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.usuario import UsuarioAdministrativo


class AuthService:
    """
    Servicio de autenticación para usuarios administrativos.
    """
    
    @staticmethod
    def authenticate(email, password):
        """
        Autentica un usuario con email y password.
        
        Args:
            email: Email del usuario
            password: Password en texto plano
            
        Returns:
            UsuarioAdministrativo: Usuario autenticado si las credenciales son válidas
            None: Si las credenciales son inválidas o el usuario está inactivo
        """
        # Buscar usuario por email
        usuario = UsuarioAdministrativo.query.filter_by(email=email).first()
        
        # Verificar que el usuario existe
        if not usuario:
            return None
        
        # Verificar que el usuario está activo
        if not usuario.activo:
            return None
        
        # Verificar password
        if not usuario.verify_password(password):
            return None
        
        # Actualizar último acceso
        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def login(usuario):
        """
        Inicia sesión para un usuario autenticado.
        
        Args:
            usuario: UsuarioAdministrativo autenticado
            
        Returns:
            bool: True si el login fue exitoso
        """
        if not usuario or not usuario.is_active:
            return False
        
        login_user(usuario)
        return True
    
    @staticmethod
    def logout():
        """
        Cierra la sesión del usuario actual.
        """
        logout_user()
    
    @staticmethod
    def get_current_user():
        """
        Obtiene el usuario actualmente autenticado.
        
        Returns:
            UsuarioAdministrativo: Usuario actual si está autenticado
            None: Si no hay usuario autenticado
        """
        if current_user.is_authenticated:
            return current_user
        return None
    
    @staticmethod
    def is_superadministrador():
        """
        Verifica si el usuario actual es superadministrador.
        
        Returns:
            bool: True si el usuario actual es superadministrador
        """
        if not current_user.is_authenticated:
            return False
        return current_user.rol == 'superadministrador'
    
    @staticmethod
    def require_superadministrador(f):
        """
        Decorador que requiere que el usuario sea superadministrador.
        
        Args:
            f: Función a decorar
            
        Returns:
            Función decorada que verifica el rol
        """
        from functools import wraps
        from flask import abort
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.rol != 'superadministrador':
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def require_admin(f):
        """
        Decorador que requiere que el usuario sea administrador o superadministrador.
        
        Args:
            f: Función a decorar
            
        Returns:
            Función decorada que verifica el rol
        """
        from functools import wraps
        from flask import abort
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.rol not in ['superadministrador', 'administrador']:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function

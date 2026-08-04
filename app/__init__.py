"""
Portal de Verificación de Cobertura y Solicitud de Instalación
Enlaces Costa Grande

Aplicación Flask principal con factory pattern.
"""

import os
import logging
from flask import Flask
from .config import config_by_name
from .extensions import db, migrate, cors, login_manager
from .cli import register_commands


def create_app(config_name=None):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración a usar 
                          ('development', 'testing', 'production')
    
    Returns:
        Flask: Instancia de la aplicación Flask configurada
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Crear instancia de Flask
    app = Flask(__name__, static_folder='../public')
    
    # Cargar configuración
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
    login_manager.login_message_category = 'warning'
    
    # Configurar sesión (30 minutos de inactividad - RNF-012)
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos en segundos
    
    # Loader para Flask-Login
    from app.models.usuario import UsuarioAdministrativo
    
    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioAdministrativo.query.get(int(user_id))
    
    # Importar modelos para que Flask-Migrate pueda detectarlos
    # Esto es necesario para que Alembic vea el esquema de la base de datos
    from . import models  # noqa: F401
    
    # Registrar comandos CLI
    register_commands(app)
    
    # Registrar blueprints
    from .routes.health import health_bp
    from .routes.auth import auth_bp
    from .routes.portal import portal_bp
    from .routes.admin import admin_bp
    from .routes.admin.municipios import municipios_bp
    from .routes.admin.colonias import colonias_bp
    from .routes.admin.cobertura import cobertura_bp
    from .routes.admin.planes import planes_bp
    from .routes.admin.disponibilidad import disponibilidad_bp
    from .routes.admin.solicitudes import solicitudes_bp
    from .routes.admin.analisis import analisis_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(municipios_bp)
    app.register_blueprint(colonias_bp)
    app.register_blueprint(cobertura_bp)
    app.register_blueprint(planes_bp)
    app.register_blueprint(disponibilidad_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(analisis_bp)
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not Found', 'message': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error', 'message': 'Error interno del servidor'}, 500
    
    app.logger.info(f'Aplicación Flask iniciada en modo {config_name}')
    
    return app

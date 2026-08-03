"""
Extensiones de Flask

Este módulo inicializa las extensiones de Flask que se usarán en la aplicación.
Se inicializan aquí para evitar importaciones circulares.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
login_manager = LoginManager()

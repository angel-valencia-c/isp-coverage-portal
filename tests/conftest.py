"""
Configuración de pytest y fixtures globales

Este módulo contiene fixtures que estarán disponibles para todos los tests.
"""

import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    """
    Fixture que crea una instancia de la aplicación para testing
    """
    app = create_app('testing')
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """
    Fixture que proporciona un cliente de testing
    """
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='function')
def db(app):
    """
    Fixture que proporciona la sesión de base de datos
    """
    with app.app_context():
        yield _db


@pytest.fixture(scope='function')
def db_session(app, db):
    """
    Fixture que proporciona una sesión de base de datos limpia para cada test.
    
    Crea las tablas antes del test y las elimina después, asegurando
    aislamiento entre tests.
    """
    with app.app_context():
        # Crear todas las tablas
        _db.create_all()
        
        # Proporcionar la sesión
        yield _db.session
        
        # Limpiar después del test
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def init_database(app):
    """
    Fixture que inicializa la base de datos con datos de prueba
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

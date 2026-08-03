"""
Tests del CRUD de Municipios
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.usuario import UsuarioAdministrativo
from app.models.municipio import Municipio
from app.services.municipio_service import MunicipioService


@pytest.fixture
def app():
    """Crear aplicación de prueba"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()


@pytest.fixture
def superadmin(app):
    """Crear superadministrador de prueba"""
    with app.app_context():
        usuario = UsuarioAdministrativo(
            nombre='Super Admin',
            email='superadmin@example.com',
            password='password123',
            rol='superadministrador',
            activo=True
        )
        db.session.add(usuario)
        db.session.commit()
        yield usuario


@pytest.fixture
def municipio_prueba(app):
    """Crear municipio de prueba"""
    with app.app_context():
        municipio = Municipio(
            nombre='Acapulco de Juárez',
            estado='Guerrero',
            activo=True
        )
        db.session.add(municipio)
        db.session.commit()
        yield municipio


class TestMunicipioService:
    """Tests del servicio de municipios"""
    
    def test_create_municipio(self, app):
        """Test de creación de municipio"""
        with app.app_context():
            municipio = MunicipioService.create('Chilpancingo', 'Guerrero')
            assert municipio is not None
            assert municipio.nombre == 'Chilpancingo'
            assert municipio.estado == 'Guerrero'
            assert municipio.activo is True
    
    def test_create_municipio_duplicado(self, app, municipio_prueba):
        """Test de creación de municipio duplicado"""
        with app.app_context():
            with pytest.raises(ValueError, match='Ya existe un municipio'):
                MunicipioService.create('Acapulco de Juárez', 'Guerrero')
    
    def test_get_all_municipios(self, app, municipio_prueba):
        """Test de obtener todos los municipios"""
        with app.app_context():
            municipios = MunicipioService.get_all()
            assert len(municipios) == 1
            assert municipios[0].nombre == 'Acapulco de Juárez'
    
    def test_get_all_incluye_inactivos(self, app, municipio_prueba):
        """Test de obtener todos los municipios incluyendo inactivos"""
        with app.app_context():
            municipio_prueba.activo = False
            db.session.commit()
            
            municipios_activos = MunicipioService.get_all(incluir_inactivos=False)
            assert len(municipios_activos) == 0
            
            municipios_todos = MunicipioService.get_all(incluir_inactivos=True)
            assert len(municipios_todos) == 1
    
    def test_get_by_id(self, app, municipio_prueba):
        """Test de obtener municipio por ID"""
        with app.app_context():
            municipio = MunicipioService.get_by_id(municipio_prueba.id)
            assert municipio is not None
            assert municipio.nombre == 'Acapulco de Juárez'
    
    def test_get_by_id_inexistente(self, app):
        """Test de obtener municipio inexistente"""
        with app.app_context():
            municipio = MunicipioService.get_by_id(999)
            assert municipio is None
    
    def test_update_municipio(self, app, municipio_prueba):
        """Test de actualizar municipio"""
        with app.app_context():
            municipio = MunicipioService.update(
                municipio_prueba.id,
                nombre='Acapulco'
            )
            assert municipio.nombre == 'Acapulco'
    
    def test_update_municipio_inexistente(self, app):
        """Test de actualizar municipio inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un municipio'):
                MunicipioService.update(999, nombre='Test')
    
    def test_deactivate_municipio(self, app, municipio_prueba):
        """Test de desactivar municipio"""
        with app.app_context():
            municipio = MunicipioService.deactivate(municipio_prueba.id)
            assert municipio.activo is False
    
    def test_activate_municipio(self, app, municipio_prueba):
        """Test de activar municipio"""
        with app.app_context():
            municipio_prueba.activo = False
            db.session.commit()
            
            municipio = MunicipioService.activate(municipio_prueba.id)
            assert municipio.activo is True


class TestMunicipiosRoutes:
    """Tests de las rutas de municipios"""
    
    def test_list_municipios_sin_login(self, client):
        """Test de listar municipios sin login"""
        response = client.get('/admin/municipios/')
        assert response.status_code == 302  # Redirige a login
    
    def test_list_municipios_con_login(self, client, superadmin, app):
        """Test de listar municipios con login"""
        with app.app_context():
            # Login
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            # Listar municipios
            response = client.get('/admin/municipios/')
            assert response.status_code == 200
            assert b'Municipios' in response.data
    
    def test_new_municipio_get(self, client, superadmin, app):
        """Test de formulario de nuevo municipio (GET)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get('/admin/municipios/new')
            assert response.status_code == 200
            assert b'Nuevo Municipio' in response.data
    
    def test_new_municipio_post(self, client, superadmin, app):
        """Test de crear municipio (POST)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post('/admin/municipios/new', data={
                'nombre': 'Chilpancingo',
                'estado': 'Guerrero'
            }, follow_redirects=False)
            
            assert response.status_code == 302  # Redirige a lista
            
            # Verificar que se creó
            municipio = Municipio.query.filter_by(nombre='Chilpancingo').first()
            assert municipio is not None
    
    def test_edit_municipio_get(self, client, superadmin, municipio_prueba, app):
        """Test de formulario de editar municipio (GET)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get(f'/admin/municipios/{municipio_prueba.id}/edit')
            assert response.status_code == 200
            assert b'Editar Municipio' in response.data
    
    def test_edit_municipio_post(self, client, superadmin, municipio_prueba, app):
        """Test de actualizar municipio (POST)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post(f'/admin/municipios/{municipio_prueba.id}/edit', data={
                'nombre': 'Acapulco',
                'estado': 'Guerrero'
            }, follow_redirects=False)
            
            assert response.status_code == 302
            
            # Verificar que se actualizó
            municipio = Municipio.query.get(municipio_prueba.id)
            assert municipio.nombre == 'Acapulco'
    
    def test_deactivate_municipio(self, client, superadmin, municipio_prueba, app):
        """Test de desactivar municipio"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post(f'/admin/municipios/{municipio_prueba.id}/deactivate', follow_redirects=False)
            assert response.status_code == 302
            
            # Verificar que se desactivó
            municipio = Municipio.query.get(municipio_prueba.id)
            assert municipio.activo is False

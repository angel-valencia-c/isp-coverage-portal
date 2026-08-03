"""
Tests del CRUD de Colonias
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.usuario import UsuarioAdministrativo
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.services.colonia_service import ColoniaService


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


@pytest.fixture
def colonia_prueba(app, municipio_prueba):
    """Crear colonia de prueba"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Centro',
            tipo='colonia',
            municipio_id=municipio_prueba.id,
            activo=True
        )
        db.session.add(colonia)
        db.session.commit()
        yield colonia


class TestColoniaService:
    """Tests del servicio de colonias"""
    
    def test_create_colonia(self, app, municipio_prueba):
        """Test de creación de colonia"""
        with app.app_context():
            colonia = ColoniaService.create(
                nombre='Las Playas',
                tipo='colonia',
                municipio_id=municipio_prueba.id
            )
            assert colonia is not None
            assert colonia.nombre == 'Las Playas'
            assert colonia.tipo == 'colonia'
            assert colonia.municipio_id == municipio_prueba.id
            assert colonia.activo is True
    
    def test_create_colonia_municipio_inexistente(self, app):
        """Test de creación de colonia con municipio inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un municipio'):
                ColoniaService.create(
                    nombre='Test',
                    tipo='colonia',
                    municipio_id=999
                )
    
    def test_create_colonia_duplicada(self, app, municipio_prueba, colonia_prueba):
        """Test de creación de colonia duplicada en el mismo municipio"""
        with app.app_context():
            with pytest.raises(ValueError, match='Ya existe una colonia'):
                ColoniaService.create(
                    nombre='Centro',
                    tipo='colonia',
                    municipio_id=municipio_prueba.id
                )
    
    def test_create_colonia_mismo_nombre_diferente_municipio(self, app, municipio_prueba, colonia_prueba):
        """Test de creación de colonia con mismo nombre en diferente municipio"""
        with app.app_context():
            # Crear otro municipio
            municipio2 = Municipio(
                nombre='Chilpancingo',
                estado='Guerrero',
                activo=True
            )
            db.session.add(municipio2)
            db.session.commit()
            
            # Debe permitir crear colonia con mismo nombre en diferente municipio
            colonia2 = ColoniaService.create(
                nombre='Centro',
                tipo='colonia',
                municipio_id=municipio2.id
            )
            assert colonia2 is not None
            assert colonia2.nombre == 'Centro'
            assert colonia2.municipio_id == municipio2.id
    
    def test_get_all_colonias(self, app, municipio_prueba, colonia_prueba):
        """Test de obtener todas las colonias"""
        with app.app_context():
            colonias = ColoniaService.get_all()
            assert len(colonias) == 1
            assert colonias[0].nombre == 'Centro'
    
    def test_get_all_por_municipio(self, app, municipio_prueba, colonia_prueba):
        """Test de obtener colonias filtradas por municipio"""
        with app.app_context():
            colonias = ColoniaService.get_all(municipio_id=municipio_prueba.id)
            assert len(colonias) == 1
            
            # Crear otro municipio con otra colonia
            municipio2 = Municipio(nombre='Otro', estado='Guerrero', activo=True)
            db.session.add(municipio2)
            db.session.commit()
            
            colonia2 = ColoniaComunidad(nombre='Otra', tipo='colonia', municipio_id=municipio2.id, activo=True)
            db.session.add(colonia2)
            db.session.commit()
            
            # Filtrar por primer municipio
            colonias = ColoniaService.get_all(municipio_id=municipio_prueba.id)
            assert len(colonias) == 1
            assert colonias[0].nombre == 'Centro'
    
    def test_get_all_incluye_inactivas(self, app, municipio_prueba, colonia_prueba):
        """Test de obtener todas las colonias incluyendo inactivas"""
        with app.app_context():
            # Desactivar colonia
            colonia = ColoniaComunidad.query.get(colonia_prueba.id)
            colonia.activo = False
            db.session.commit()
            
            colonias_activas = ColoniaService.get_all(incluir_inactivos=False)
            assert len(colonias_activas) == 0
            
            colonias_todas = ColoniaService.get_all(incluir_inactivos=True)
            assert len(colonias_todas) == 1
    
    def test_get_by_id(self, app, colonia_prueba):
        """Test de obtener colonia por ID"""
        with app.app_context():
            colonia = ColoniaService.get_by_id(colonia_prueba.id)
            assert colonia is not None
            assert colonia.nombre == 'Centro'
    
    def test_get_by_id_inexistente(self, app):
        """Test de obtener colonia inexistente"""
        with app.app_context():
            colonia = ColoniaService.get_by_id(999)
            assert colonia is None
    
    def test_update_colonia(self, app, colonia_prueba):
        """Test de actualizar colonia"""
        with app.app_context():
            colonia = ColoniaService.update(
                colonia_prueba.id,
                nombre='Centro Histórico'
            )
            assert colonia.nombre == 'Centro Histórico'
    
    def test_update_colonia_inexistente(self, app):
        """Test de actualizar colonia inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una colonia'):
                ColoniaService.update(999, nombre='Test')
    
    def test_deactivate_colonia(self, app, colonia_prueba):
        """Test de desactivar colonia"""
        with app.app_context():
            colonia = ColoniaService.deactivate(colonia_prueba.id)
            assert colonia.activo is False
    
    def test_activate_colonia(self, app, colonia_prueba):
        """Test de activar colonia"""
        with app.app_context():
            colonia_prueba.activo = False
            db.session.commit()
            
            colonia = ColoniaService.activate(colonia_prueba.id)
            assert colonia.activo is True
    
    def test_activate_colonia_municipio_inactivo(self, app, colonia_prueba, municipio_prueba):
        """Test de activar colonia con municipio inactivo"""
        with app.app_context():
            # Desactivar municipio
            municipio = Municipio.query.get(municipio_prueba.id)
            municipio.activo = False
            db.session.commit()
            
            # Desactivar colonia
            colonia = ColoniaComunidad.query.get(colonia_prueba.id)
            colonia.activo = False
            db.session.commit()
            
            # Intentar activar colonia debe fallar
            with pytest.raises(ValueError, match='No se puede activar'):
                ColoniaService.activate(colonia_prueba.id)


class TestColoniasRoutes:
    """Tests de las rutas de colonias"""
    
    def test_list_colonias_sin_login(self, client):
        """Test de listar colonias sin login"""
        response = client.get('/admin/colonias/')
        assert response.status_code == 302  # Redirige a login
    
    def test_list_colonias_con_login(self, client, superadmin, app):
        """Test de listar colonias con login"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get('/admin/colonias/')
            assert response.status_code == 200
            assert b'Colonias' in response.data
    
    def test_new_colonia_get(self, client, superadmin, app):
        """Test de formulario de nueva colonia (GET)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get('/admin/colonias/new')
            assert response.status_code == 200
            assert b'Nueva Colonia' in response.data
    
    def test_new_colonia_post(self, client, superadmin, municipio_prueba, app):
        """Test de crear colonia (POST)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post('/admin/colonias/new', data={
                'nombre': 'Las Playas',
                'tipo': 'colonia',
                'municipio_id': municipio_prueba.id
            }, follow_redirects=False)
            
            assert response.status_code == 302  # Redirige a lista
            
            # Verificar que se creó
            colonia = ColoniaComunidad.query.filter_by(nombre='Las Playas').first()
            assert colonia is not None
    
    def test_edit_colonia_get(self, client, superadmin, colonia_prueba, app):
        """Test de formulario de editar colonia (GET)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get(f'/admin/colonias/{colonia_prueba.id}/edit')
            assert response.status_code == 200
            assert b'Editar Colonia' in response.data
    
    def test_edit_colonia_post(self, client, superadmin, colonia_prueba, app):
        """Test de actualizar colonia (POST)"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post(f'/admin/colonias/{colonia_prueba.id}/edit', data={
                'nombre': 'Centro Histórico',
                'tipo': 'colonia',
                'municipio_id': colonia_prueba.municipio_id
            }, follow_redirects=False)
            
            assert response.status_code == 302
            
            # Verificar que se actualizó
            colonia = ColoniaComunidad.query.get(colonia_prueba.id)
            assert colonia.nombre == 'Centro Histórico'
    
    def test_deactivate_colonia(self, client, superadmin, colonia_prueba, app):
        """Test de desactivar colonia"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.post(f'/admin/colonias/{colonia_prueba.id}/deactivate', follow_redirects=False)
            assert response.status_code == 302
            
            # Verificar que se desactivó
            colonia = ColoniaComunidad.query.get(colonia_prueba.id)
            assert colonia.activo is False
    
    def test_filter_by_municipio(self, client, superadmin, municipio_prueba, colonia_prueba, app):
        """Test de filtrar colonias por municipio"""
        with app.app_context():
            client.post('/admin/login', data={
                'email': 'superadmin@example.com',
                'password': 'password123'
            })
            
            response = client.get(f'/admin/colonias/?municipio_id={municipio_prueba.id}')
            assert response.status_code == 200
            assert b'Centro' in response.data

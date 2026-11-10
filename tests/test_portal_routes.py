"""
Tests de las Rutas del Portal Público
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura


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
def municipio(app):
    """Crear municipio de prueba"""
    with app.app_context():
        municipio = Municipio(nombre='Acapulco', estado='Guerrero', activo=True)
        db.session.add(municipio)
        db.session.commit()
        yield municipio


@pytest.fixture
def colonia_con_cobertura(app, municipio):
    """Crear colonia con cobertura"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Centro',
            tipo='colonia',
            municipio_id=municipio.id,
            activo=True
        )
        db.session.add(colonia)
        db.session.commit()
        
        cobertura = Cobertura(
            colonia_id=colonia.id,
            activa=True,
            tipo_cobertura='total'
        )
        db.session.add(cobertura)
        db.session.commit()
        
        yield colonia


@pytest.fixture
def colonia_sin_cobertura(app, municipio):
    """Crear colonia sin cobertura"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Las Playas',
            tipo='colonia',
            municipio_id=municipio.id,
            activo=True
        )
        db.session.add(colonia)
        db.session.commit()
        yield colonia


class TestPortalRoutes:
    """Tests de las rutas del portal público"""
    
    def test_index_page(self, client, municipio):
        """Test de la página principal"""
        with client.session_transaction() as sess:
            pass
        
        response = client.get('/')
        assert response.status_code == 200
        assert b'Internet Regional' in response.data
        assert b'Verifica tu Cobertura' in response.data
    
    def test_api_municipios(self, client, municipio):
        """Test de API de municipios"""
        response = client.get('/api/municipios')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['nombre'] == 'Acapulco'
    
    def test_api_colonias(self, client, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de API de colonias"""
        response = client.get(f'/api/colonias/{municipio.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 2
    
    def test_api_colonias_solo_con_cobertura(self, client, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de API de colonias solo con cobertura"""
        response = client.get(f'/api/colonias/{municipio.id}?solo_con_cobertura=true')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['nombre'] == 'Centro'
    
    def test_api_verificar_cobertura_con_cobertura(self, client, colonia_con_cobertura):
        """Test de API de verificación de cobertura con cobertura"""
        response = client.get(f'/api/verificar-cobertura/{colonia_con_cobertura.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['tiene_cobertura'] is True
        assert data['colonia']['nombre'] == 'Centro'
    
    def test_api_verificar_cobertura_sin_cobertura(self, client, colonia_sin_cobertura):
        """Test de API de verificación de cobertura sin cobertura"""
        response = client.get(f'/api/verificar-cobertura/{colonia_sin_cobertura.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['tiene_cobertura'] is False
    
    def test_api_buscar_colonias(self, client, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de API de búsqueda de colonias"""
        response = client.get('/api/buscar-colonias?q=centro')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['nombre'] == 'Centro'
    
    def test_api_buscar_municipios(self, client, municipio):
        """Test de API de búsqueda de municipios"""
        response = client.get('/api/buscar-municipios?q=acapulco')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['nombre'] == 'Acapulco'

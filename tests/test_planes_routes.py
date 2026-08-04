"""
Tests de las Rutas de Planes del Portal Público
"""
import pytest
from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.plan import Plan
from app.models.disponibilidad_plan import DisponibilidadPlanZona


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
def colonia(app, municipio):
    """Crear colonia de prueba"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Centro',
            tipo='colonia',
            municipio_id=municipio.id,
            activo=True
        )
        db.session.add(colonia)
        db.session.commit()
        yield colonia


@pytest.fixture
def cobertura(app, colonia):
    """Crear cobertura de prueba"""
    with app.app_context():
        cobertura = Cobertura(
            colonia_id=colonia.id,
            activa=True,
            tipo_cobertura='total'
        )
        db.session.add(cobertura)
        db.session.commit()
        yield cobertura


@pytest.fixture
def plan(app):
    """Crear plan de prueba"""
    with app.app_context():
        plan = Plan(
            nombre='Básico',
            velocidad_descarga=20,
            velocidad_subida=5,
            precio_mensual=Decimal('299.99'),
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


@pytest.fixture
def disponibilidad(app, cobertura, plan):
    """Crear disponibilidad de plan"""
    with app.app_context():
        disponibilidad = DisponibilidadPlanZona(
            cobertura_id=cobertura.id,
            plan_id=plan.id,
            costo_instalacion=Decimal('500.00')
        )
        db.session.add(disponibilidad)
        db.session.commit()
        yield disponibilidad


class TestPlanesRoutes:
    """Tests de las rutas de planes del portal público"""
    
    def test_planes_page_con_cobertura(self, client, colonia, cobertura, disponibilidad):
        """Test de página de planes con cobertura"""
        response = client.get(f'/planes/{colonia.id}')
        assert response.status_code == 200
        assert b'Planes Disponibles' in response.data
        # Verificar que el plan está en la página (usando ASCII)
        assert b'Basico' in response.data or b'299' in response.data
    
    def test_planes_page_sin_cobertura(self, client, colonia):
        """Test de página de planes sin cobertura"""
        response = client.get(f'/planes/{colonia.id}')
        assert response.status_code == 200
        assert b'Sin cobertura' in response.data or b'sin_cobertura' in response.data
    
    def test_api_planes(self, client, cobertura, disponibilidad):
        """Test de API de planes"""
        response = client.get(f'/api/planes/{cobertura.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['nombre'] == 'Básico'
        assert data[0]['velocidad_descarga'] == 20
        assert data[0]['precio_mensual'] == 299.99
        assert data[0]['costo_instalacion'] == 500.00
    
    def test_api_cotizacion(self, client, cobertura, disponibilidad):
        """Test de API de cotización"""
        plan = Plan.query.first()
        
        response = client.get(f'/api/cotizacion/{cobertura.id}/{plan.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['plan_nombre'] == 'Básico'
        assert data['costo_instalacion'] == 500.00
        assert data['precio_mensual'] == 299.99
        assert data['total_inicial'] == 799.99
    
    def test_api_cotizacion_plan_no_disponible(self, client, cobertura, plan):
        """Test de API de cotización con plan no disponible"""
        response = client.get(f'/api/cotizacion/{cobertura.id}/{plan.id}')
        assert response.status_code == 404

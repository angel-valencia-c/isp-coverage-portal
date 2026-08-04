"""
Tests del Servicio de Búsqueda Pública
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.services.busqueda_publica_service import BusquedaPublicaService


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


class TestBusquedaPublicaService:
    """Tests del servicio de búsqueda pública"""
    
    def test_get_municipios_activos(self, app, municipio):
        """Test de obtener municipios activos"""
        with app.app_context():
            municipios = BusquedaPublicaService.get_municipios_activos()
            assert len(municipios) == 1
            assert municipios[0].nombre == 'Acapulco'
    
    def test_get_municipios_activos_excluye_inactivos(self, app, municipio):
        """Test de que excluye municipios inactivos"""
        with app.app_context():
            # Crear municipio inactivo
            municipio_inactivo = Municipio(nombre='Inactivo', estado='Guerrero', activo=False)
            db.session.add(municipio_inactivo)
            db.session.commit()
            
            municipios = BusquedaPublicaService.get_municipios_activos()
            assert len(municipios) == 1
            assert municipios[0].nombre == 'Acapulco'
    
    def test_get_colonias_por_municipio(self, app, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de obtener colonias por municipio"""
        with app.app_context():
            colonias = BusquedaPublicaService.get_colonias_por_municipio(municipio.id)
            assert len(colonias) == 2
    
    def test_get_colonias_por_municipio_solo_con_cobertura(self, app, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de obtener solo colonias con cobertura"""
        with app.app_context():
            colonias = BusquedaPublicaService.get_colonias_por_municipio(
                municipio.id,
                solo_con_cobertura=True
            )
            assert len(colonias) == 1
            assert colonias[0].nombre == 'Centro'
    
    def test_verificar_cobertura_con_cobertura(self, app, colonia_con_cobertura):
        """Test de verificar cobertura cuando existe"""
        with app.app_context():
            resultado = BusquedaPublicaService.verificar_cobertura(colonia_con_cobertura.id)
            assert resultado['tiene_cobertura'] is True
            assert resultado['cobertura'] is not None
            assert resultado['colonia'].nombre == 'Centro'
    
    def test_verificar_cobertura_sin_cobertura(self, app, colonia_sin_cobertura):
        """Test de verificar cobertura cuando no existe"""
        with app.app_context():
            resultado = BusquedaPublicaService.verificar_cobertura(colonia_sin_cobertura.id)
            assert resultado['tiene_cobertura'] is False
            assert resultado['cobertura'] is None
            assert resultado['colonia'].nombre == 'Las Playas'
    
    def test_verificar_cobertura_colonia_inexistente(self, app):
        """Test de verificar cobertura de colonia inexistente"""
        with app.app_context():
            resultado = BusquedaPublicaService.verificar_cobertura(999)
            assert resultado['tiene_cobertura'] is False
            assert resultado['colonia'] is None
    
    def test_buscar_colonias(self, app, municipio, colonia_con_cobertura, colonia_sin_cobertura):
        """Test de búsqueda de colonias"""
        with app.app_context():
            resultados = BusquedaPublicaService.buscar_colonias('centro')
            assert len(resultados) == 1
            assert resultados[0].nombre == 'Centro'
    
    def test_buscar_colonias_sin_resultados(self, app, municipio, colonia_con_cobertura):
        """Test de búsqueda sin resultados"""
        with app.app_context():
            resultados = BusquedaPublicaService.buscar_colonias('xyz')
            assert len(resultados) == 0
    
    def test_buscar_colonias_termino_corto(self, app, municipio, colonia_con_cobertura):
        """Test de búsqueda con término muy corto"""
        with app.app_context():
            resultados = BusquedaPublicaService.buscar_colonias('c')
            assert len(resultados) == 0
    
    def test_buscar_municipios(self, app, municipio):
        """Test de búsqueda de municipios"""
        with app.app_context():
            resultados = BusquedaPublicaService.buscar_municipios('acapulco')
            assert len(resultados) == 1
            assert resultados[0].nombre == 'Acapulco'
    
    def test_buscar_municipios_sin_resultados(self, app, municipio):
        """Test de búsqueda de municipios sin resultados"""
        with app.app_context():
            resultados = BusquedaPublicaService.buscar_municipios('xyz')
            assert len(resultados) == 0

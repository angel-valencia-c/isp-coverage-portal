"""
Tests del Servicio de Análisis de Demanda
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.plan import Plan
from app.models.solicitud import SolicitudInstalacion
from app.services.analisis_demanda_service import AnalisisDemandaService


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
            precio_mensual=299.99,
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


@pytest.fixture
def solicitudes(app, municipio, colonia, cobertura, plan):
    """Crear múltiples solicitudes de prueba"""
    with app.app_context():
        solicitudes = []
        
        # 3 solicitudes pendientes con cobertura
        for i in range(3):
            solicitud = SolicitudInstalacion(
                nombre_prospecto=f'Cliente {i+1}',
                telefono_contacto=f'744123456{i}',
                direccion_especifica=f'Calle {i+1}',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            db.session.add(solicitud)
            solicitudes.append(solicitud)
        
        # 2 solicitudes contactadas con cobertura
        for i in range(2):
            solicitud = SolicitudInstalacion(
                nombre_prospecto=f'Cliente {i+4}',
                telefono_contacto=f'744123456{i+3}',
                direccion_especifica=f'Calle {i+4}',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                estado='contactado',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            db.session.add(solicitud)
            solicitudes.append(solicitud)
        
        db.session.commit()
        yield solicitudes


class TestAnalisisDemandaService:
    """Tests del servicio de análisis de demanda"""
    
    def test_get_demand_por_municipio(self, app, solicitudes):
        """Test de demanda por municipio"""
        with app.app_context():
            demand = AnalisisDemandaService.get_demand_por_municipio()
            
            assert len(demand) == 1
            assert demand[0]['municipio_nombre'] == 'Acapulco'
            assert demand[0]['total_solicitudes'] == 5
    
    def test_get_demand_por_municipio_con_filtro_estado(self, app, solicitudes):
        """Test de demanda por municipio con filtro de estado"""
        with app.app_context():
            demand = AnalisisDemandaService.get_demand_por_municipio(estado='pendiente')
            
            assert len(demand) == 1
            assert demand[0]['total_solicitudes'] == 3
    
    def test_get_demand_por_colonia(self, app, solicitudes):
        """Test de demanda por colonia"""
        with app.app_context():
            demand = AnalisisDemandaService.get_demand_por_colonia()
            
            assert len(demand) == 1
            assert demand[0]['colonia_nombre'] == 'Centro'
            assert demand[0]['municipio_nombre'] == 'Acapulco'
            assert demand[0]['total_solicitudes'] == 5
    
    def test_get_demand_por_colonia_con_filtro_municipio(self, app, solicitudes):
        """Test de demanda por colonia con filtro de municipio"""
        with app.app_context():
            municipio = Municipio.query.first()
            demand = AnalisisDemandaService.get_demand_por_colonia(municipio_id=municipio.id)
            
            assert len(demand) == 1
            assert demand[0]['total_solicitudes'] == 5
    
    def test_get_demand_con_vs_sin_cobertura(self, app, solicitudes):
        """Test de demanda con vs sin cobertura"""
        with app.app_context():
            demand = AnalisisDemandaService.get_demand_con_vs_sin_cobertura()
            
            assert demand['con_cobertura'] == 5
            assert demand['sin_cobertura'] == 0
            assert demand['total'] == 5
    
    def test_get_top_colonias(self, app, solicitudes):
        """Test de top colonias"""
        with app.app_context():
            top = AnalisisDemandaService.get_top_colonias(limit=10)
            
            assert len(top) == 1
            assert top[0]['colonia_nombre'] == 'Centro'
            assert top[0]['total_solicitudes'] == 5
    
    def test_get_demand_por_estado(self, app, solicitudes):
        """Test de demanda por estado"""
        with app.app_context():
            demand = AnalisisDemandaService.get_demand_por_estado()
            
            assert demand['pendiente'] == 3
            assert demand['contactado'] == 2
    
    def test_get_demand_por_estado_con_filtro_municipio(self, app, solicitudes):
        """Test de demanda por estado con filtro de municipio"""
        with app.app_context():
            municipio = Municipio.query.first()
            demand = AnalisisDemandaService.get_demand_por_estado(municipio_id=municipio.id)
            
            assert demand['pendiente'] == 3
            assert demand['contactado'] == 2
    
    def test_get_demand_sin_solicitudes(self, app):
        """Test de demanda sin solicitudes"""
        with app.app_context():
            demand_municipio = AnalisisDemandaService.get_demand_por_municipio()
            demand_colonia = AnalisisDemandaService.get_demand_por_colonia()
            demand_cobertura = AnalisisDemandaService.get_demand_con_vs_sin_cobertura()
            top_colonias = AnalisisDemandaService.get_top_colonias()
            demand_estado = AnalisisDemandaService.get_demand_por_estado()
            
            assert len(demand_municipio) == 0
            assert len(demand_colonia) == 0
            assert demand_cobertura['con_cobertura'] == 0
            assert demand_cobertura['sin_cobertura'] == 0
            assert len(top_colonias) == 0
            assert len(demand_estado) == 0

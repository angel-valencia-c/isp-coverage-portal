"""
Tests del Servicio de Dashboard
"""
import pytest
from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.plan import Plan
from app.models.solicitud import SolicitudInstalacion
from app.models.disponibilidad_plan import DisponibilidadPlanZona
from app.services.dashboard_service import DashboardService


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
        municipio = Municipio(nombre='Test Municipio', estado='Test Estado')
        db.session.add(municipio)
        db.session.commit()
        yield municipio


@pytest.fixture
def colonia(app, municipio):
    """Crear colonia de prueba"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Test Colonia',
            tipo='colonia',
            municipio_id=municipio.id
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
            nombre='Plan Test',
            velocidad_descarga=100,
            velocidad_subida=50,
            precio_mensual=Decimal('499.99'),
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


@pytest.fixture
def solicitud(app, municipio, colonia):
    """Crear solicitud de prueba"""
    with app.app_context():
        solicitud = SolicitudInstalacion(
            nombre_prospecto='Test Prospecto',
            telefono_contacto='1234567890',
            direccion_especifica='Test Address',
            municipio_id=municipio.id,
            colonia_id=colonia.id,
            estado='pendiente',
            origen='portal'
        )
        db.session.add(solicitud)
        db.session.commit()
        yield solicitud


class TestDashboardService:
    """Tests del servicio de dashboard"""
    
    def test_get_metricas_generales(self, app, municipio, colonia, cobertura, plan, solicitud):
        """Test de obtención de métricas generales"""
        with app.app_context():
            metricas = DashboardService.get_metricas_generales()
            
            assert metricas['total_municipios'] == 1
            assert metricas['total_colonias'] == 1
            assert metricas['total_coberturas_activas'] == 1
            assert metricas['total_planes_activos'] == 1
            assert metricas['total_solicitudes'] == 1
            assert metricas['solicitudes_pendientes'] == 1
            assert metricas['solicitudes_contactadas'] == 0
            assert metricas['solicitudes_agendadas'] == 0
    
    def test_get_metricas_sin_datos(self, app):
        """Test de métricas sin datos"""
        with app.app_context():
            metricas = DashboardService.get_metricas_generales()
            
            assert metricas['total_municipios'] == 0
            assert metricas['total_colonias'] == 0
            assert metricas['total_coberturas_activas'] == 0
            assert metricas['total_planes_activos'] == 0
            assert metricas['total_solicitudes'] == 0
    
    def test_get_solicitudes_recientes(self, app, municipio, colonia, solicitud):
        """Test de obtención de solicitudes recientes"""
        with app.app_context():
            # Crear más solicitudes
            for i in range(5):
                sol = SolicitudInstalacion(
                    nombre_prospecto=f'Prospecto {i}',
                    telefono_contacto=f'123456789{i}',
                    direccion_especifica=f'Address {i}',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    estado='pendiente',
                    origen='portal'
                )
                db.session.add(sol)
            db.session.commit()
            
            solicitudes = DashboardService.get_solicitudes_recientes(limit=3)
            
            assert len(solicitudes) == 3
    
    def test_get_resumen_por_estado(self, app, municipio, colonia):
        """Test de resumen por estado"""
        with app.app_context():
            # Crear solicitudes en diferentes estados
            estados = ['pendiente', 'pendiente', 'contactado', 'agendado', 'cancelado']
            for estado in estados:
                sol = SolicitudInstalacion(
                    nombre_prospecto=f'Prospecto {estado}',
                    telefono_contacto=f'12345678{estado[:2]}',
                    direccion_especifica=f'Address {estado}',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    estado=estado,
                    origen='portal'
                )
                db.session.add(sol)
            db.session.commit()
            
            resumen = DashboardService.get_resumen_por_estado()
            
            assert resumen['pendiente'] == 2
            assert resumen['contactado'] == 1
            assert resumen['agendado'] == 1
            assert resumen['cancelado'] == 1
            assert resumen['duplicado'] == 0
    
    def test_get_vista_jerarquica(self, app, municipio, colonia, cobertura, plan):
        """Test de vista jerárquica"""
        with app.app_context():
            # Asociar plan a cobertura
            disponibilidad = DisponibilidadPlanZona(
                cobertura_id=cobertura.id,
                plan_id=plan.id,
                costo_instalacion=Decimal('500.00')
            )
            db.session.add(disponibilidad)
            db.session.commit()
            
            vista = DashboardService.get_vista_jerarquica()
            
            assert len(vista) == 1
            assert vista[0]['municipio'].id == municipio.id
            assert len(vista[0]['colonias']) == 1
            assert vista[0]['colonias'][0]['colonia'].id == colonia.id
            assert vista[0]['colonias'][0]['cobertura'] is not None
            assert len(vista[0]['colonias'][0]['cobertura']['planes']) == 1
    
    def test_get_vista_jerarquica_filtro_municipio(self, app, municipio, colonia):
        """Test de vista jerárquica con filtro por municipio"""
        with app.app_context():
            # Crear otro municipio
            municipio2 = Municipio(nombre='Test Municipio 2', estado='Test Estado')
            db.session.add(municipio2)
            db.session.commit()
            
            colonia2 = ColoniaComunidad(
                nombre='Test Colonia 2',
                tipo='colonia',
                municipio_id=municipio2.id
            )
            db.session.add(colonia2)
            db.session.commit()
            
            # Filtrar por primer municipio
            vista = DashboardService.get_vista_jerarquica(municipio_id=municipio.id)
            
            assert len(vista) == 1
            assert vista[0]['municipio'].id == municipio.id
    
    def test_coberturas_sin_planes_count(self, app, municipio, colonia, cobertura, plan):
        """Test de conteo de coberturas sin planes"""
        with app.app_context():
            # Crear otra cobertura sin planes
            colonia2 = ColoniaComunidad(
                nombre='Test Colonia 2',
                tipo='colonia',
                municipio_id=municipio.id
            )
            db.session.add(colonia2)
            db.session.commit()
            
            cobertura2 = Cobertura(
                colonia_id=colonia2.id,
                activa=True,
                tipo_cobertura='total'
            )
            db.session.add(cobertura2)
            db.session.commit()
            
            # Asociar plan a primera cobertura
            disponibilidad = DisponibilidadPlanZona(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            db.session.add(disponibilidad)
            db.session.commit()
            
            metricas = DashboardService.get_metricas_generales()
            
            assert metricas['coberturas_sin_planes'] == 1

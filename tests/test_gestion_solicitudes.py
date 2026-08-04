"""
Tests del Servicio de Gestión de Solicitudes
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.plan import Plan
from app.models.solicitud import SolicitudInstalacion
from app.services.gestion_solicitudes_service import GestionSolicitudesService


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
def solicitud(app, municipio, colonia, plan):
    """Crear solicitud de prueba"""
    with app.app_context():
        solicitud = SolicitudInstalacion(
            nombre_prospecto='Juan Pérez',
            telefono_contacto='7441234567',
            direccion_especifica='Calle Principal #123',
            municipio_id=municipio.id,
            colonia_id=colonia.id,
            plan_id=plan.id,
            costo_instalacion_cotizado=500.00,
            precio_mensual_cotizado=299.99,
            estado='pendiente',
            origen='portal',
            tipo='solicitud_cobertura'
        )
        db.session.add(solicitud)
        db.session.commit()
        yield solicitud


class TestGestionSolicitudesService:
    """Tests del servicio de gestión de solicitudes"""
    
    def test_get_solicitudes(self, app, solicitud):
        """Test de obtener todas las solicitudes"""
        with app.app_context():
            solicitudes = GestionSolicitudesService.get_solicitudes()
            assert len(solicitudes) == 1
            assert solicitudes[0].nombre_prospecto == 'Juan Pérez'
    
    def test_get_solicitudes_filtro_estado(self, app, solicitud):
        """Test de filtrar solicitudes por estado"""
        with app.app_context():
            # Filtrar por estado pendiente
            solicitudes = GestionSolicitudesService.get_solicitudes(estado='pendiente')
            assert len(solicitudes) == 1
            
            # Filtrar por estado contactado (no debe haber)
            solicitudes = GestionSolicitudesService.get_solicitudes(estado='contactado')
            assert len(solicitudes) == 0
    
    def test_get_solicitud_by_id(self, app, solicitud):
        """Test de obtener solicitud por ID"""
        with app.app_context():
            solicitud_obtenida = GestionSolicitudesService.get_solicitud_by_id(solicitud.id)
            assert solicitud_obtenida is not None
            assert solicitud_obtenida.id == solicitud.id
    
    def test_get_solicitud_by_id_inexistente(self, app):
        """Test de obtener solicitud inexistente"""
        with app.app_context():
            solicitud = GestionSolicitudesService.get_solicitud_by_id(999)
            assert solicitud is None
    
    def test_cambiar_estado(self, app, solicitud):
        """Test de cambiar estado de solicitud"""
        with app.app_context():
            solicitud_actualizada = GestionSolicitudesService.cambiar_estado(
                solicitud_id=solicitud.id,
                nuevo_estado='contactado'
            )
            assert solicitud_actualizada.estado == 'contactado'
    
    def test_cambiar_estado_invalido(self, app, solicitud):
        """Test de cambiar a estado inválido"""
        with app.app_context():
            with pytest.raises(ValueError, match='Estado inválido'):
                GestionSolicitudesService.cambiar_estado(
                    solicitud_id=solicitud.id,
                    nuevo_estado='invalido'
                )
    
    def test_cambiar_estado_solicitud_inexistente(self, app):
        """Test de cambiar estado de solicitud inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una solicitud'):
                GestionSolicitudesService.cambiar_estado(
                    solicitud_id=999,
                    nuevo_estado='contactado'
                )
    
    def test_marcar_como_duplicada(self, app, municipio, colonia, plan):
        """Test de marcar solicitud como duplicada"""
        with app.app_context():
            # Crear dos solicitudes
            solicitud1 = SolicitudInstalacion(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            solicitud2 = SolicitudInstalacion(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Secundaria #456',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            db.session.add(solicitud1)
            db.session.add(solicitud2)
            db.session.commit()
            
            # Marcar segunda como duplicada de la primera
            solicitud_duplicada = GestionSolicitudesService.marcar_como_duplicada(
                solicitud_id=solicitud2.id,
                solicitud_original_id=solicitud1.id
            )
            
            assert solicitud_duplicada.estado == 'duplicado'
            assert solicitud_duplicada.solicitud_duplicada_de == solicitud1.id
    
    def test_exportar_a_csv(self, app, solicitud):
        """Test de exportar solicitudes a CSV"""
        with app.app_context():
            solicitudes = GestionSolicitudesService.get_solicitudes()
            csv_content = GestionSolicitudesService.exportar_a_csv(solicitudes)
            
            assert csv_content is not None
            assert 'Juan Pérez' in csv_content
            assert '7441234567' in csv_content
    
    def test_get_estadisticas(self, app, solicitud):
        """Test de obtener estadísticas"""
        with app.app_context():
            estadisticas = GestionSolicitudesService.get_estadisticas()
            
            assert estadisticas['total'] == 1
            assert estadisticas['por_estado']['pendiente'] == 1
            assert estadisticas['por_origen']['portal'] == 1
            assert estadisticas['por_tipo']['solicitud_cobertura'] == 1

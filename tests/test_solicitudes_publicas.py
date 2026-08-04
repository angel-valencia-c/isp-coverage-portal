"""
Tests del Servicio de Solicitudes Públicas
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.plan import Plan
from app.models.disponibilidad_plan import DisponibilidadPlanZona
from app.models.solicitud import SolicitudInstalacion
from app.services.solicitudes_publicas_service import SolicitudesPublicasService


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


class TestSolicitudesPublicasService:
    """Tests del servicio de solicitudes públicas"""
    
    def test_crear_solicitud(self, app, municipio, colonia, plan):
        """Test de creación de solicitud"""
        with app.app_context():
            solicitud = SolicitudesPublicasService.crear_solicitud(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                costo_instalacion_cotizado=500.00,
                precio_mensual_cotizado=299.99
            )
            
            assert solicitud is not None
            assert solicitud.nombre_prospecto == 'Juan Pérez'
            assert solicitud.telefono_contacto == '7441234567'
            assert solicitud.estado == 'pendiente'
            assert solicitud.origen == 'portal'
            assert solicitud.tipo == 'solicitud_cobertura'
    
    def test_crear_solicitud_sin_plan(self, app, municipio, colonia):
        """Test de creación de solicitud sin plan (lead)"""
        with app.app_context():
            solicitud = SolicitudesPublicasService.crear_solicitud(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=None
            )
            
            assert solicitud is not None
            assert solicitud.tipo == 'lead_sin_cobertura'
            assert solicitud.plan_id is None
    
    def test_crear_solicitud_nombre_vacio(self, app, municipio, colonia, plan):
        """Test de creación con nombre vacío"""
        with app.app_context():
            with pytest.raises(ValueError, match='El nombre es obligatorio'):
                SolicitudesPublicasService.crear_solicitud(
                    nombre_prospecto='',
                    telefono_contacto='7441234567',
                    direccion_especifica='Calle Principal #123',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    plan_id=plan.id
                )
    
    def test_crear_solicitud_telefono_invalido(self, app, municipio, colonia, plan):
        """Test de creación con teléfono inválido"""
        with app.app_context():
            with pytest.raises(ValueError, match='El teléfono debe tener 10 dígitos'):
                SolicitudesPublicasService.crear_solicitud(
                    nombre_prospecto='Juan Pérez',
                    telefono_contacto='744123456',  # Solo 9 dígitos
                    direccion_especifica='Calle Principal #123',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    plan_id=plan.id
                )
    
    def test_crear_solicitud_direccion_vacia(self, app, municipio, colonia, plan):
        """Test de creación con dirección vacía"""
        with app.app_context():
            with pytest.raises(ValueError, match='La dirección es obligatoria'):
                SolicitudesPublicasService.crear_solicitud(
                    nombre_prospecto='Juan Pérez',
                    telefono_contacto='7441234567',
                    direccion_especifica='',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    plan_id=plan.id
                )
    
    def test_crear_solicitud_duplicada(self, app, municipio, colonia, plan):
        """Test de creación de solicitud duplicada"""
        with app.app_context():
            # Crear primera solicitud
            SolicitudesPublicasService.crear_solicitud(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id
            )
            
            # Intentar crear segunda solicitud con mismo teléfono
            with pytest.raises(ValueError, match='Ya existe una solicitud pendiente'):
                SolicitudesPublicasService.crear_solicitud(
                    nombre_prospecto='Juan Pérez',
                    telefono_contacto='7441234567',
                    direccion_especifica='Calle Secundaria #456',
                    municipio_id=municipio.id,
                    colonia_id=colonia.id,
                    plan_id=plan.id
                )
    
    def test_crear_solicitud_telefono_antiguo_no_es_duplicado(self, app, municipio, colonia, plan):
        """Test de que solicitud antigua no es duplicada"""
        with app.app_context():
            # Crear solicitud antigua (hace 8 días)
            solicitud_antigua = SolicitudInstalacion(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura',
                fecha_creacion=datetime.utcnow() - timedelta(days=8)
            )
            db.session.add(solicitud_antigua)
            db.session.commit()
            
            # Crear nueva solicitud con mismo teléfono (debe permitir)
            solicitud_nueva = SolicitudesPublicasService.crear_solicitud(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Secundaria #456',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id
            )
            
            assert solicitud_nueva is not None
    
    def test_crear_lead_sin_cobertura(self, app, municipio, colonia):
        """Test de creación de lead sin cobertura"""
        with app.app_context():
            lead = SolicitudesPublicasService.crear_lead_sin_cobertura(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                municipio_id=municipio.id,
                colonia_id=colonia.id
            )
            
            assert lead is not None
            assert lead.tipo == 'lead_sin_cobertura'
            assert lead.plan_id is None
    
    def test_verificar_duplicado(self, app, municipio, colonia, plan):
        """Test de verificación de duplicado"""
        with app.app_context():
            # Sin solicitudes
            assert SolicitudesPublicasService.verificar_duplicado('7441234567') is False
            
            # Crear solicitud
            SolicitudesPublicasService.crear_solicitud(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio.id,
                colonia_id=colonia.id,
                plan_id=plan.id
            )
            
            # Verificar duplicado
            assert SolicitudesPublicasService.verificar_duplicado('7441234567') is True
            assert SolicitudesPublicasService.verificar_duplicado('7449876543') is False

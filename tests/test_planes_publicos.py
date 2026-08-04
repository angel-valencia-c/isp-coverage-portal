"""
Tests del Servicio de Planes Públicos
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
from app.models.configuracion import Configuracion
from app.services.planes_publicos_service import PlanesPublicosService


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
def plan_basico(app):
    """Crear plan básico de prueba"""
    with app.app_context():
        plan = Plan(
            nombre='Básico',
            velocidad_descarga=20,
            velocidad_subida=5,
            precio_mensual=Decimal('299.99'),
            descripcion='Plan básico de internet',
            orden=1,
            destacado=False,
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


@pytest.fixture
def plan_premium(app):
    """Crear plan premium de prueba"""
    with app.app_context():
        plan = Plan(
            nombre='Premium',
            velocidad_descarga=100,
            velocidad_subida=50,
            precio_mensual=Decimal('799.99'),
            descripcion='Plan premium de internet',
            orden=2,
            destacado=True,
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


@pytest.fixture
def disponibilidad_basico(app, cobertura, plan_basico):
    """Crear disponibilidad del plan básico"""
    with app.app_context():
        disponibilidad = DisponibilidadPlanZona(
            cobertura_id=cobertura.id,
            plan_id=plan_basico.id,
            costo_instalacion=Decimal('500.00')
        )
        db.session.add(disponibilidad)
        db.session.commit()
        yield disponibilidad


@pytest.fixture
def disponibilidad_premium(app, cobertura, plan_premium):
    """Crear disponibilidad del plan premium"""
    with app.app_context():
        disponibilidad = DisponibilidadPlanZona(
            cobertura_id=cobertura.id,
            plan_id=plan_premium.id,
            costo_instalacion=Decimal('800.00')
        )
        db.session.add(disponibilidad)
        db.session.commit()
        yield disponibilidad


class TestPlanesPublicosService:
    """Tests del servicio de planes públicos"""
    
    def test_get_planes_disponibles(self, app, cobertura, disponibilidad_basico, disponibilidad_premium):
        """Test de obtener planes disponibles"""
        with app.app_context():
            planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
            
            assert len(planes_info) == 2
            # Verificar orden (por campo 'orden')
            assert planes_info[0]['plan'].nombre == 'Básico'
            assert planes_info[1]['plan'].nombre == 'Premium'
    
    def test_get_planes_disponibles_con_costo_personalizado(self, app, cobertura, disponibilidad_basico):
        """Test de obtener planes con costo de instalación personalizado"""
        with app.app_context():
            planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
            
            assert len(planes_info) == 1
            assert planes_info[0]['costo_instalacion'] == Decimal('500.00')
    
    def test_get_planes_disponibles_sin_costo_personalizado(self, app, cobertura, plan_basico):
        """Test de obtener planes sin costo personalizado (usa costo estándar base)"""
        with app.app_context():
            # Crear disponibilidad sin costo personalizado
            disponibilidad = DisponibilidadPlanZona(
                cobertura_id=cobertura.id,
                plan_id=plan_basico.id,
                costo_instalacion=None
            )
            db.session.add(disponibilidad)
            
            # Configurar costo estándar base
            config = Configuracion(
                clave='costo_estandar_base',
                valor='1000.00'
            )
            db.session.add(config)
            db.session.commit()
            
            planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
            
            assert len(planes_info) == 1
            assert planes_info[0]['costo_instalacion'] == Decimal('1000.00')
    
    def test_get_costo_estandar_base(self, app):
        """Test de obtener costo estándar base"""
        with app.app_context():
            # Sin configuración
            costo = PlanesPublicosService.get_costo_estandar_base()
            assert costo == Decimal('0')
            
            # Con configuración
            config = Configuracion(
                clave='costo_estandar_base',
                valor='1500.00'
            )
            db.session.add(config)
            db.session.commit()
            
            costo = PlanesPublicosService.get_costo_estandar_base()
            assert costo == Decimal('1500.00')
    
    def test_calcular_cotizacion(self, app, cobertura, disponibilidad_basico):
        """Test de calcular cotización"""
        with app.app_context():
            plan_basico = Plan.query.filter_by(nombre='Básico').first()
            
            cotizacion = PlanesPublicosService.calcular_cotizacion(
                plan_basico.id,
                cobertura.id
            )
            
            assert cotizacion is not None
            assert cotizacion['plan'].nombre == 'Básico'
            assert cotizacion['costo_instalacion'] == Decimal('500.00')
            assert cotizacion['precio_mensual'] == Decimal('299.99')
            assert cotizacion['total_inicial'] == Decimal('799.99')
    
    def test_calcular_cotizacion_plan_inexistente(self, app, cobertura):
        """Test de calcular cotización con plan inexistente"""
        with app.app_context():
            cotizacion = PlanesPublicosService.calcular_cotizacion(999, cobertura.id)
            assert cotizacion is None
    
    def test_calcular_cotizacion_plan_no_disponible(self, app, cobertura, plan_basico):
        """Test de calcular cotización con plan no disponible en la zona"""
        with app.app_context():
            cotizacion = PlanesPublicosService.calcular_cotizacion(
                plan_basico.id,
                cobertura.id
            )
            assert cotizacion is None
    
    def test_get_plan_destacado(self, app, cobertura, disponibilidad_basico, disponibilidad_premium):
        """Test de obtener plan destacado"""
        with app.app_context():
            planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
            plan_destacado = PlanesPublicosService.get_plan_destacado(planes_info)
            
            assert plan_destacado is not None
            assert plan_destacado['plan'].nombre == 'Premium'
            assert plan_destacado['plan'].destacado is True
    
    def test_get_plan_destacado_sin_destacado(self, app, cobertura, disponibilidad_basico):
        """Test de obtener plan destacado cuando no hay ninguno destacado"""
        with app.app_context():
            planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
            plan_destacado = PlanesPublicosService.get_plan_destacado(planes_info)
            
            assert plan_destacado is None

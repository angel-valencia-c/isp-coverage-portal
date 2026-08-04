"""
Tests del Servicio de Disponibilidad de Planes
"""
import pytest
from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models.cobertura import Cobertura
from app.models.colonia import ColoniaComunidad
from app.models.municipio import Municipio
from app.models.plan import Plan
from app.models.disponibilidad_plan import DisponibilidadPlanZona
from app.models.configuracion import Configuracion
from app.services.disponibilidad_plan_service import DisponibilidadPlanService


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


class TestDisponibilidadPlanService:
    """Tests del servicio de disponibilidad de planes"""
    
    def test_create_disponibilidad(self, app, cobertura, plan):
        """Test de creación de disponibilidad"""
        with app.app_context():
            disponibilidad = DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id,
                costo_instalacion=500.00
            )
            
            assert disponibilidad is not None
            assert disponibilidad.cobertura_id == cobertura.id
            assert disponibilidad.plan_id == plan.id
            assert disponibilidad.costo_instalacion == Decimal('500.00')
    
    def test_create_disponibilidad_sin_costo(self, app, cobertura, plan):
        """Test de creación de disponibilidad sin costo personalizado"""
        with app.app_context():
            disponibilidad = DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            assert disponibilidad is not None
            assert disponibilidad.costo_instalacion is None
    
    def test_create_disponibilidad_cobertura_inexistente(self, app, plan):
        """Test de creación con cobertura inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una cobertura'):
                DisponibilidadPlanService.create(
                    cobertura_id=999,
                    plan_id=plan.id
                )
    
    def test_create_disponibilidad_plan_inexistente(self, app, cobertura):
        """Test de creación con plan inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un plan'):
                DisponibilidadPlanService.create(
                    cobertura_id=cobertura.id,
                    plan_id=999
                )
    
    def test_create_disponibilidad_duplicada(self, app, cobertura, plan):
        """Test de creación de disponibilidad duplicada"""
        with app.app_context():
            # Crear primera vez
            DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            # Intentar crear segunda vez
            with pytest.raises(ValueError, match='ya está asociado'):
                DisponibilidadPlanService.create(
                    cobertura_id=cobertura.id,
                    plan_id=plan.id
                )
    
    def test_get_by_cobertura(self, app, cobertura, plan):
        """Test de obtener disponibilidades por cobertura"""
        with app.app_context():
            # Crear disponibilidad
            DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            disponibilidades = DisponibilidadPlanService.get_by_cobertura(cobertura.id)
            
            assert len(disponibilidades) == 1
            assert disponibilidades[0]['plan'].id == plan.id
    
    def test_get_planes_disponibles_para_asociar(self, app, cobertura, plan):
        """Test de obtener planes disponibles para asociar"""
        with app.app_context():
            # Crear otro plan
            plan2 = Plan(
                nombre='Plan Test 2',
                velocidad_descarga=200,
                velocidad_subida=100,
                precio_mensual=Decimal('699.99'),
                activo=True
            )
            db.session.add(plan2)
            db.session.commit()
            
            # Asociar primer plan
            DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            # Obtener planes disponibles
            planes_disponibles = DisponibilidadPlanService.get_planes_disponibles_para_asociar(cobertura.id)
            
            assert len(planes_disponibles) == 1
            assert planes_disponibles[0].id == plan2.id
    
    def test_update_costo(self, app, cobertura, plan):
        """Test de actualizar costo de instalación"""
        with app.app_context():
            # Crear disponibilidad
            disponibilidad = DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id,
                costo_instalacion=500.00
            )
            
            # Actualizar costo
            disponibilidad_actualizada = DisponibilidadPlanService.update_costo(
                disponibilidad_id=disponibilidad.id,
                costo_instalacion=600.00
            )
            
            assert disponibilidad_actualizada.costo_instalacion == Decimal('600.00')
    
    def test_remove_disponibilidad(self, app, cobertura, plan):
        """Test de eliminar disponibilidad"""
        with app.app_context():
            # Crear disponibilidad
            disponibilidad = DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            # Eliminar
            result = DisponibilidadPlanService.remove(disponibilidad.id)
            
            assert result is True
            
            # Verificar que se eliminó
            disponibilidades = DisponibilidadPlanService.get_by_cobertura(cobertura.id)
            assert len(disponibilidades) == 0
    
    def test_get_costo_estandar_base(self, app):
        """Test de obtener costo estándar base"""
        with app.app_context():
            # Configurar costo base
            config = Configuracion(
                clave='costo_estandar_base',
                valor='1000.00'
            )
            db.session.add(config)
            db.session.commit()
            
            costo_base = DisponibilidadPlanService.get_costo_estandar_base()
            
            assert costo_base == Decimal('1000.00')
    
    def test_set_costo_estandar_base(self, app):
        """Test de configurar costo estándar base"""
        with app.app_context():
            # Configurar costo base
            DisponibilidadPlanService.set_costo_estandar_base(1500.00)
            
            # Verificar
            config = Configuracion.query.filter_by(clave='costo_estandar_base').first()
            assert config is not None
            assert config.valor == '1500.0'
    
    def test_get_coberturas_sin_planes(self, app, cobertura, plan, colonia, municipio):
        """Test de obtener coberturas sin planes"""
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
            DisponibilidadPlanService.create(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            )
            
            # Obtener coberturas sin planes
            coberturas_sin_planes = DisponibilidadPlanService.get_coberturas_sin_planes()
            
            assert len(coberturas_sin_planes) == 1
            assert coberturas_sin_planes[0].id == cobertura2.id

"""
Tests del Servicio de Planes
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.plan import Plan
from app.services.plan_service import PlanService


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
def plan_basico(app):
    """Crear plan básico de prueba"""
    with app.app_context():
        plan = Plan(
            nombre='Básico',
            velocidad_descarga=20,
            velocidad_subida=5,
            precio_mensual=299.99,
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
            precio_mensual=799.99,
            descripcion='Plan premium de internet',
            orden=2,
            destacado=True,
            activo=True
        )
        db.session.add(plan)
        db.session.commit()
        yield plan


class TestPlanService:
    """Tests del servicio de planes"""
    
    def test_create_plan(self, app):
        """Test de creación de plan"""
        with app.app_context():
            plan = PlanService.create(
                nombre='Básico',
                velocidad_descarga=20,
                velocidad_subida=5,
                precio_mensual=299.99,
                descripcion='Plan básico',
                orden=1,
                destacado=False
            )
            
            assert plan is not None
            assert plan.nombre == 'Básico'
            assert plan.velocidad_descarga == 20
            assert plan.velocidad_subida == 5
            assert float(plan.precio_mensual) == 299.99
            assert plan.descripcion == 'Plan básico'
            assert plan.orden == 1
            assert plan.destacado is False
            assert plan.activo is True
    
    def test_create_plan_duplicado(self, app, plan_basico):
        """Test de creación de plan duplicado"""
        with app.app_context():
            with pytest.raises(ValueError, match='Ya existe un plan con el nombre'):
                PlanService.create(
                    nombre='Básico',
                    velocidad_descarga=30,
                    velocidad_subida=10,
                    precio_mensual=399.99
                )
    
    def test_get_all_planes(self, app, plan_basico, plan_premium):
        """Test de obtener todos los planes"""
        with app.app_context():
            planes = PlanService.get_all()
            
            assert len(planes) == 2
            # Verificar orden (por orden y nombre)
            assert planes[0].nombre == 'Básico'
            assert planes[1].nombre == 'Premium'
    
    def test_get_all_planes_incluir_inactivos(self, app, plan_basico, plan_premium):
        """Test de obtener planes incluyendo inactivos"""
        with app.app_context():
            # Desactivar un plan
            plan = Plan.query.get(plan_basico.id)
            plan.activo = False
            db.session.commit()
            
            # Sin incluir inactivos
            planes_activos = PlanService.get_all(incluir_inactivos=False)
            assert len(planes_activos) == 1
            assert planes_activos[0].nombre == 'Premium'
            
            # Incluyendo inactivos
            planes_todos = PlanService.get_all(incluir_inactivos=True)
            assert len(planes_todos) == 2
    
    def test_get_by_id(self, app, plan_basico):
        """Test de obtener plan por ID"""
        with app.app_context():
            plan = PlanService.get_by_id(plan_basico.id)
            
            assert plan is not None
            assert plan.id == plan_basico.id
            assert plan.nombre == 'Básico'
    
    def test_get_by_id_inexistente(self, app):
        """Test de obtener plan inexistente"""
        with app.app_context():
            plan = PlanService.get_by_id(999)
            assert plan is None
    
    def test_update_plan(self, app, plan_basico):
        """Test de actualizar plan"""
        with app.app_context():
            plan = PlanService.update(
                plan_id=plan_basico.id,
                nombre='Básico Plus',
                velocidad_descarga=30,
                velocidad_subida=10,
                precio_mensual=399.99,
                descripcion='Plan básico mejorado',
                orden=2,
                destacado=True
            )
            
            assert plan.nombre == 'Básico Plus'
            assert plan.velocidad_descarga == 30
            assert plan.velocidad_subida == 10
            assert float(plan.precio_mensual) == 399.99
            assert plan.descripcion == 'Plan básico mejorado'
            assert plan.orden == 2
            assert plan.destacado is True
    
    def test_update_plan_nombre_duplicado(self, app, plan_basico, plan_premium):
        """Test de actualizar plan con nombre duplicado"""
        with app.app_context():
            with pytest.raises(ValueError, match='Ya existe un plan con el nombre'):
                PlanService.update(
                    plan_id=plan_basico.id,
                    nombre='Premium'
                )
    
    def test_update_plan_inexistente(self, app):
        """Test de actualizar plan inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un plan con ID'):
                PlanService.update(
                    plan_id=999,
                    nombre='Test'
                )
    
    def test_deactivate_plan(self, app, plan_basico):
        """Test de desactivar plan"""
        with app.app_context():
            plan = PlanService.deactivate(plan_basico.id)
            
            assert plan is not None
            assert plan.activo is False
    
    def test_deactivate_plan_inexistente(self, app):
        """Test de desactivar plan inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un plan con ID'):
                PlanService.deactivate(999)
    
    def test_activate_plan(self, app, plan_basico):
        """Test de activar plan"""
        with app.app_context():
            # Desactivar primero
            plan_basico.activo = False
            db.session.commit()
            
            # Activar
            plan = PlanService.activate(plan_basico.id)
            
            assert plan is not None
            assert plan.activo is True
    
    def test_activate_plan_inexistente(self, app):
        """Test de activar plan inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe un plan con ID'):
                PlanService.activate(999)
    
    def test_plan_destacado(self, app):
        """Test de plan destacado"""
        with app.app_context():
            plan = PlanService.create(
                nombre='Destacado',
                velocidad_descarga=50,
                velocidad_subida=25,
                precio_mensual=599.99,
                destacado=True
            )
            
            assert plan.destacado is True
    
    def test_plan_orden(self, app):
        """Test de orden de planes"""
        with app.app_context():
            # Crear planes con diferente orden
            plan1 = PlanService.create(
                nombre='Plan 1',
                velocidad_descarga=20,
                velocidad_subida=5,
                precio_mensual=299.99,
                orden=3
            )
            
            plan2 = PlanService.create(
                nombre='Plan 2',
                velocidad_descarga=30,
                velocidad_subida=10,
                precio_mensual=399.99,
                orden=1
            )
            
            plan3 = PlanService.create(
                nombre='Plan 3',
                velocidad_descarga=40,
                velocidad_subida=20,
                precio_mensual=499.99,
                orden=2
            )
            
            # Verificar orden
            planes = PlanService.get_all()
            assert planes[0].nombre == 'Plan 2'  # orden=1
            assert planes[1].nombre == 'Plan 3'  # orden=2
            assert planes[2].nombre == 'Plan 1'  # orden=3

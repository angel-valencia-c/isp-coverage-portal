"""
Tests del Servicio de Notas de Solicitudes
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.plan import Plan
from app.models.solicitud import SolicitudInstalacion
from app.models.usuario import UsuarioAdministrativo
from app.services.notas_solicitudes_service import NotasSolicitudesService


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
            estado='pendiente',
            origen='portal',
            tipo='solicitud_cobertura'
        )
        db.session.add(solicitud)
        db.session.commit()
        yield solicitud


@pytest.fixture
def usuario(app):
    """Crear usuario de prueba"""
    with app.app_context():
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            rol='administrador',
            activo=True
        )
        usuario.password = 'password123'
        db.session.add(usuario)
        db.session.commit()
        yield usuario


class TestNotasSolicitudesService:
    """Tests del servicio de notas de solicitudes"""
    
    def test_crear_nota(self, app, solicitud, usuario):
        """Test de creación de nota"""
        with app.app_context():
            nota = NotasSolicitudesService.crear_nota(
                solicitud_id=solicitud.id,
                texto='Primera nota de seguimiento',
                usuario_id=usuario.id
            )
            
            assert nota is not None
            assert nota.texto == 'Primera nota de seguimiento'
            assert nota.solicitud_id == solicitud.id
            assert nota.creado_por == usuario.id
    
    def test_crear_nota_solicitud_inexistente(self, app, usuario):
        """Test de creación de nota con solicitud inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una solicitud'):
                NotasSolicitudesService.crear_nota(
                    solicitud_id=999,
                    texto='Nota de prueba',
                    usuario_id=usuario.id
                )
    
    def test_crear_nota_texto_vacio(self, app, solicitud, usuario):
        """Test de creación de nota con texto vacío"""
        with app.app_context():
            with pytest.raises(ValueError, match='El texto de la nota es obligatorio'):
                NotasSolicitudesService.crear_nota(
                    solicitud_id=solicitud.id,
                    texto='',
                    usuario_id=usuario.id
                )
    
    def test_get_notas_by_solicitud(self, app, solicitud, usuario):
        """Test de obtener notas de una solicitud"""
        with app.app_context():
            # Crear varias notas
            NotasSolicitudesService.crear_nota(solicitud.id, 'Nota 1', usuario.id)
            NotasSolicitudesService.crear_nota(solicitud.id, 'Nota 2', usuario.id)
            NotasSolicitudesService.crear_nota(solicitud.id, 'Nota 3', usuario.id)
            
            notas = NotasSolicitudesService.get_notas_by_solicitud(solicitud.id, orden='desc')
            
            assert len(notas) == 3
            # Verificar orden descendente (más reciente primero)
            assert notas[0].texto == 'Nota 3'
            assert notas[1].texto == 'Nota 2'
            assert notas[2].texto == 'Nota 1'
    
    def test_get_notas_by_solicitud_ascendente(self, app, solicitud, usuario):
        """Test de obtener notas en orden ascendente"""
        with app.app_context():
            # Crear varias notas
            NotasSolicitudesService.crear_nota(solicitud.id, 'Nota 1', usuario.id)
            NotasSolicitudesService.crear_nota(solicitud.id, 'Nota 2', usuario.id)
            
            notas = NotasSolicitudesService.get_notas_by_solicitud(solicitud.id, orden='asc')
            
            assert len(notas) == 2
            # Verificar orden ascendente (más antigua primero)
            assert notas[0].texto == 'Nota 1'
            assert notas[1].texto == 'Nota 2'
    
    def test_get_nota_by_id(self, app, solicitud, usuario):
        """Test de obtener nota por ID"""
        with app.app_context():
            nota_creada = NotasSolicitudesService.crear_nota(
                solicitud_id=solicitud.id,
                texto='Nota de prueba',
                usuario_id=usuario.id
            )
            
            nota_obtenida = NotasSolicitudesService.get_nota_by_id(nota_creada.id)
            
            assert nota_obtenida is not None
            assert nota_obtenida.id == nota_creada.id
            assert nota_obtenida.texto == 'Nota de prueba'
    
    def test_get_nota_by_id_inexistente(self, app):
        """Test de obtener nota inexistente"""
        with app.app_context():
            nota = NotasSolicitudesService.get_nota_by_id(999)
            assert nota is None
    
    def test_eliminar_nota(self, app, solicitud, usuario):
        """Test de eliminar nota"""
        with app.app_context():
            # Crear nota
            nota = NotasSolicitudesService.crear_nota(
                solicitud_id=solicitud.id,
                texto='Nota a eliminar',
                usuario_id=usuario.id
            )
            
            # Eliminar nota
            resultado = NotasSolicitudesService.eliminar_nota(nota.id)
            
            assert resultado is True
            
            # Verificar que se eliminó
            nota_eliminada = NotasSolicitudesService.get_nota_by_id(nota.id)
            assert nota_eliminada is None
    
    def test_eliminar_nota_inexistente(self, app):
        """Test de eliminar nota inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una nota'):
                NotasSolicitudesService.eliminar_nota(999)

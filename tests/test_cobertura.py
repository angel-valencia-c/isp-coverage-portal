"""
Tests del Servicio de Cobertura
"""
import pytest
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.usuario import UsuarioAdministrativo
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.solicitud import SolicitudInstalacion
from app.services.cobertura_service import CoberturaService


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
def superadmin(app):
    """Crear superadministrador de prueba"""
    with app.app_context():
        usuario = UsuarioAdministrativo(
            nombre='Super Admin',
            email='superadmin@example.com',
            password='password123',
            rol='superadministrador',
            activo=True
        )
        db.session.add(usuario)
        db.session.commit()
        yield usuario


@pytest.fixture
def municipio_prueba(app):
    """Crear municipio de prueba"""
    with app.app_context():
        municipio = Municipio(
            nombre='Acapulco de Juárez',
            estado='Guerrero',
            activo=True
        )
        db.session.add(municipio)
        db.session.commit()
        yield municipio


@pytest.fixture
def colonia_prueba(app, municipio_prueba):
    """Crear colonia de prueba"""
    with app.app_context():
        colonia = ColoniaComunidad(
            nombre='Centro',
            tipo='colonia',
            municipio_id=municipio_prueba.id,
            activo=True
        )
        db.session.add(colonia)
        db.session.commit()
        yield colonia


@pytest.fixture
def cobertura_prueba(app, colonia_prueba):
    """Crear cobertura de prueba"""
    with app.app_context():
        cobertura = Cobertura(
            colonia_id=colonia_prueba.id,
            activa=True,
            tipo_cobertura='total',
            fecha_activacion=datetime.utcnow()
        )
        db.session.add(cobertura)
        db.session.commit()
        yield cobertura


class TestCoberturaService:
    """Tests del servicio de cobertura"""
    
    def test_activate_cobertura(self, app, colonia_prueba):
        """Test de activación de cobertura"""
        with app.app_context():
            cobertura = CoberturaService.activate(
                colonia_id=colonia_prueba.id,
                tipo_cobertura='total'
            )
            assert cobertura is not None
            assert cobertura.colonia_id == colonia_prueba.id
            assert cobertura.activa is True
            assert cobertura.tipo_cobertura == 'total'
            assert cobertura.fecha_activacion is not None
    
    def test_activate_cobertura_colonia_inexistente(self, app):
        """Test de activación con colonia inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una colonia'):
                CoberturaService.activate(colonia_id=999)
    
    def test_activate_cobertura_colonia_inactiva(self, app, municipio_prueba):
        """Test de activación con colonia inactiva"""
        with app.app_context():
            colonia = ColoniaComunidad(
                nombre='Inactiva',
                tipo='colonia',
                municipio_id=municipio_prueba.id,
                activo=False
            )
            db.session.add(colonia)
            db.session.commit()
            
            with pytest.raises(ValueError, match='está inactiva'):
                CoberturaService.activate(colonia_id=colonia.id)
    
    def test_activate_cobertura_duplicada(self, app, colonia_prueba, cobertura_prueba):
        """Test de activación con cobertura ya existente"""
        with app.app_context():
            with pytest.raises(ValueError, match='ya tiene cobertura activa'):
                CoberturaService.activate(colonia_id=colonia_prueba.id)
    
    def test_activate_cobertura_con_notas(self, app, colonia_prueba):
        """Test de activación con notas"""
        with app.app_context():
            cobertura = CoberturaService.activate(
                colonia_id=colonia_prueba.id,
                tipo_cobertura='total',
                notas='Cobertura completa con fibra óptica'
            )
            assert cobertura.notas == 'Cobertura completa con fibra óptica'
    
    def test_reactivate_cobertura(self, app, colonia_prueba):
        """Test de reactivación de cobertura"""
        with app.app_context():
            # Crear cobertura inactiva
            cobertura = Cobertura(
                colonia_id=colonia_prueba.id,
                activa=False,
                tipo_cobertura='total',
                fecha_activacion=datetime.utcnow(),
                fecha_desactivacion=datetime.utcnow()
            )
            db.session.add(cobertura)
            db.session.commit()
            
            # Reactivar
            cobertura_reactivada = CoberturaService.activate(
                colonia_id=colonia_prueba.id,
                tipo_cobertura='parcial'
            )
            assert cobertura_reactivada.activa is True
            assert cobertura_reactivada.tipo_cobertura == 'parcial'
            assert cobertura_reactivada.fecha_desactivacion is None
    
    def test_deactivate_cobertura(self, app, cobertura_prueba):
        """Test de desactivación de cobertura"""
        with app.app_context():
            cobertura, info = CoberturaService.deactivate(
                colonia_id=cobertura_prueba.colonia_id
            )
            assert cobertura is not None
            assert cobertura.activa is False
            assert cobertura.fecha_desactivacion is not None
            assert info['tiene_pendientes'] is False
    
    def test_deactivate_cobertura_colonia_inexistente(self, app):
        """Test de desactivación con colonia inexistente"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe una colonia'):
                CoberturaService.deactivate(colonia_id=999)
    
    def test_deactivate_cobertura_no_existente(self, app, colonia_prueba):
        """Test de desactivación sin cobertura"""
        with app.app_context():
            with pytest.raises(ValueError, match='no tiene cobertura'):
                CoberturaService.deactivate(colonia_id=colonia_prueba.id)
    
    def test_deactivate_cobertura_con_solicitudes_pendientes(self, app, cobertura_prueba, municipio_prueba):
        """Test de desactivación con solicitudes pendientes (RN-021)"""
        with app.app_context():
            # Crear solicitud pendiente
            solicitud = SolicitudInstalacion(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio_prueba.id,
                colonia_id=cobertura_prueba.colonia_id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            db.session.add(solicitud)
            db.session.commit()
            
            # Intentar desactivar sin forzar
            cobertura, info = CoberturaService.deactivate(
                colonia_id=cobertura_prueba.colonia_id,
                forzar=False
            )
            assert cobertura is None  # No se desactivó
            assert info['tiene_pendientes'] is True
            assert info['cantidad'] == 1
            assert info['requiere_confirmacion'] is True
            
            # Verificar que la cobertura sigue activa
            cobertura_original = Cobertura.query.get(cobertura_prueba.id)
            assert cobertura_original.activa is True
    
    def test_deactivate_cobertura_forzar_con_solicitudes(self, app, cobertura_prueba, municipio_prueba):
        """Test de desactivación forzada con solicitudes pendientes"""
        with app.app_context():
            # Crear solicitud pendiente
            solicitud = SolicitudInstalacion(
                nombre_prospecto='Juan Pérez',
                telefono_contacto='7441234567',
                direccion_especifica='Calle Principal #123',
                municipio_id=municipio_prueba.id,
                colonia_id=cobertura_prueba.colonia_id,
                estado='pendiente',
                origen='portal',
                tipo='solicitud_cobertura'
            )
            db.session.add(solicitud)
            db.session.commit()
            
            # Desactivar forzando
            cobertura, info = CoberturaService.deactivate(
                colonia_id=cobertura_prueba.colonia_id,
                forzar=True
            )
            assert cobertura is not None
            assert cobertura.activa is False
            assert info['tiene_pendientes'] is True
            assert info['requiere_confirmacion'] is False
    
    def test_get_by_colonia(self, app, cobertura_prueba):
        """Test de obtener cobertura por colonia"""
        with app.app_context():
            cobertura = CoberturaService.get_by_colonia(cobertura_prueba.colonia_id)
            assert cobertura is not None
            assert cobertura.id == cobertura_prueba.id
    
    def test_get_by_colonia_no_existente(self, app, colonia_prueba):
        """Test de obtener cobertura inexistente"""
        with app.app_context():
            cobertura = CoberturaService.get_by_colonia(colonia_prueba.id)
            assert cobertura is None
    
    def test_get_all(self, app, cobertura_prueba):
        """Test de obtener todas las coberturas"""
        with app.app_context():
            coberturas = CoberturaService.get_all()
            assert len(coberturas) == 1
            assert coberturas[0].id == cobertura_prueba.id
    
    def test_get_all_incluye_inactivas(self, app, cobertura_prueba):
        """Test de obtener todas las coberturas incluyendo inactivas"""
        with app.app_context():
            # Recargar y desactivar
            cobertura = Cobertura.query.get(cobertura_prueba.id)
            cobertura.activa = False
            db.session.commit()
            
            coberturas_activas = CoberturaService.get_all(incluir_inactivas=False)
            assert len(coberturas_activas) == 0
            
            coberturas_todas = CoberturaService.get_all(incluir_inactivas=True)
            assert len(coberturas_todas) == 1
    
    def test_update_notas(self, app, cobertura_prueba):
        """Test de actualizar notas"""
        with app.app_context():
            cobertura = CoberturaService.update_notas(
                colonia_id=cobertura_prueba.colonia_id,
                notas='Nuevas notas de prueba'
            )
            assert cobertura.notas == 'Nuevas notas de prueba'
    
    def test_update_notas_cobertura_inexistente(self, app, colonia_prueba):
        """Test de actualizar notas sin cobertura"""
        with app.app_context():
            with pytest.raises(ValueError, match='No existe cobertura'):
                CoberturaService.update_notas(
                    colonia_id=colonia_prueba.id,
                    notas='Test'
                )
    
    def test_update_tipo(self, app, cobertura_prueba):
        """Test de actualizar tipo de cobertura"""
        with app.app_context():
            cobertura = CoberturaService.update_tipo(
                colonia_id=cobertura_prueba.colonia_id,
                tipo_cobertura='parcial'
            )
            assert cobertura.tipo_cobertura == 'parcial'
    
    def test_update_tipo_invalido(self, app, cobertura_prueba):
        """Test de actualizar tipo inválido"""
        with app.app_context():
            with pytest.raises(ValueError, match='Tipo de cobertura inválido'):
                CoberturaService.update_tipo(
                    colonia_id=cobertura_prueba.colonia_id,
                    tipo_cobertura='invalido'
                )
    
    def test_get_coberturas_con_info(self, app, cobertura_prueba, municipio_prueba):
        """Test de obtener coberturas con información completa"""
        with app.app_context():
            coberturas_info = CoberturaService.get_coberturas_con_info()
            assert len(coberturas_info) == 1
            
            info = coberturas_info[0]
            assert 'cobertura' in info
            assert 'colonia' in info
            assert 'municipio' in info
            assert 'solicitudes_pendientes' in info
            assert info['municipio'].id == municipio_prueba.id
            assert info['solicitudes_pendientes'] == 0
    
    def test_get_coberturas_con_info_filtro_municipio(self, app, cobertura_prueba, municipio_prueba):
        """Test de filtrar coberturas por municipio"""
        with app.app_context():
            # Crear otro municipio con cobertura
            municipio2 = Municipio(nombre='Chilpancingo', estado='Guerrero', activo=True)
            db.session.add(municipio2)
            db.session.commit()
            
            colonia2 = ColoniaComunidad(
                nombre='Otra',
                tipo='colonia',
                municipio_id=municipio2.id,
                activo=True
            )
            db.session.add(colonia2)
            db.session.commit()
            
            cobertura2 = Cobertura(
                colonia_id=colonia2.id,
                activa=True,
                tipo_cobertura='total',
                fecha_activacion=datetime.utcnow()
            )
            db.session.add(cobertura2)
            db.session.commit()
            
            # Filtrar por primer municipio
            coberturas_info = CoberturaService.get_coberturas_con_info(
                municipio_id=municipio_prueba.id
            )
            assert len(coberturas_info) == 1
            assert coberturas_info[0]['municipio'].id == municipio_prueba.id

"""
Tests para el modelo UsuarioAdministrativo

Verifica la creación, autenticación y campos de auditoría del modelo.
"""
import pytest
from datetime import datetime
from app.models.usuario import UsuarioAdministrativo
from app.extensions import db


class TestUsuarioAdministrativoModel:
    """Tests para el modelo UsuarioAdministrativo"""
    
    def test_crear_usuario_basico(self, app, db_session):
        """Test: Se puede crear un usuario básico con password"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123',
            rol='superadministrador'
        )
        db_session.add(usuario)
        db_session.commit()
        
        assert usuario.id is not None
        assert usuario.nombre == 'Admin Test'
        assert usuario.email == 'admin@test.com'
        assert usuario.rol == 'superadministrador'
        assert usuario.activo is True
    
    def test_password_se_hashea(self, app, db_session):
        """Test: El password se hashea automáticamente al asignarlo"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        
        # El password_hash debe estar configurado
        assert usuario._password_hash is not None
        assert usuario._password_hash != 'password123'
        assert len(usuario._password_hash) > 20  # Los hashes son largos
    
    def test_verificar_password_correcto(self, app, db_session):
        """Test: verify_password retorna True para password correcto"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        
        assert usuario.verify_password('password123') is True
    
    def test_verificar_password_incorrecto(self, app, db_session):
        """Test: verify_password retorna False para password incorrecto"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        
        assert usuario.verify_password('wrongpassword') is False
    
    def test_password_no_es_legible(self, app, db_session):
        """Test: No se puede leer el password directamente"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        
        with pytest.raises(AttributeError) as exc_info:
            _ = usuario.password
        
        assert 'password is not a readable attribute' in str(exc_info.value)
    
    def test_cambiar_password(self, app, db_session):
        """Test: Se puede cambiar el password de un usuario"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        # Cambiar password
        usuario.password = 'newpassword456'
        db_session.commit()
        
        # Verificar que el nuevo password funciona
        assert usuario.verify_password('newpassword456') is True
        assert usuario.verify_password('password123') is False
    
    def test_email_unico(self, app, db_session):
        """Test: El email debe ser único"""
        usuario1 = UsuarioAdministrativo(
            nombre='Admin 1',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario1)
        db_session.commit()
        
        usuario2 = UsuarioAdministrativo(
            nombre='Admin 2',
            email='admin@test.com',  # Mismo email
            password='password456'
        )
        db_session.add(usuario2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_roles_validos(self, app, db_session):
        """Test: Los roles deben ser de la lista de roles válidos"""
        for rol in UsuarioAdministrativo.ROLES_VALIDOS:
            usuario = UsuarioAdministrativo(
                nombre=f'Admin {rol}',
                email=f'{rol}@test.com',
                password='password123',
                rol=rol
            )
            db_session.add(usuario)
            db_session.commit()
            
            assert usuario.rol == rol
            db_session.delete(usuario)
            db_session.commit()
    
    def test_usuario_activo_por_defecto(self, app, db_session):
        """Test: Los usuarios son activos por defecto"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        # Recargar desde la base de datos para obtener los valores por defecto
        usuario_db = db_session.query(UsuarioAdministrativo).filter_by(email='admin@test.com').first()
        assert usuario_db.activo is True
    
    def test_desactivar_usuario(self, app, db_session):
        """Test: Se puede desactivar un usuario"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        usuario.activo = False
        db_session.commit()
        
        assert usuario.activo is False
    
    def test_fecha_creacion_se_genera_automaticamente(self, app, db_session):
        """Test: fecha_creacion se genera automáticamente"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        assert usuario.fecha_creacion is not None
        assert isinstance(usuario.fecha_creacion, datetime)
    
    def test_fecha_modificacion_se_actualiza(self, app, db_session):
        """Test: fecha_modificacion se actualiza al modificar el usuario"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        fecha_original = usuario.fecha_modificacion
        
        # Modificar el usuario
        usuario.nombre = 'Admin Modificado'
        db_session.commit()
        
        assert usuario.fecha_modificacion is not None
        assert usuario.fecha_modificacion >= fecha_original
    
    def test_ultimo_acceso_nullable(self, app, db_session):
        """Test: ultimo_acceso es nullable por defecto"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        
        assert usuario.ultimo_acceso is None
    
    def test_registrar_ultimo_acceso(self, app, db_session):
        """Test: Se puede registrar el último acceso"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123'
        )
        db_session.add(usuario)
        db_session.commit()
        
        ahora = datetime.utcnow()
        usuario.ultimo_acceso = ahora
        db_session.commit()
        
        assert usuario.ultimo_acceso == ahora
    
    def test_to_dict_no_incluye_password(self, app, db_session):
        """Test: to_dict no incluye el password_hash por seguridad"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123',
            rol='superadministrador'
        )
        db_session.add(usuario)
        db_session.commit()
        
        data = usuario.to_dict()
        
        assert 'password_hash' not in data
        assert '_password_hash' not in data
        assert 'password' not in data
        assert data['nombre'] == 'Admin Test'
        assert data['email'] == 'admin@test.com'
        assert data['rol'] == 'superadministrador'
    
    def test_to_dict_incluye_campos_basicos(self, app, db_session):
        """Test: to_dict incluye todos los campos básicos"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123',
            rol='administrador'
        )
        db_session.add(usuario)
        db_session.commit()
        
        data = usuario.to_dict()
        
        assert 'id' in data
        assert 'nombre' in data
        assert 'email' in data
        assert 'rol' in data
        assert 'activo' in data
        assert 'fecha_creacion' in data
        assert 'fecha_modificacion' in data
    
    def test_repr(self, app, db_session):
        """Test: __repr__ muestra información útil"""
        usuario = UsuarioAdministrativo(
            nombre='Admin Test',
            email='admin@test.com',
            password='password123',
            rol='superadministrador'
        )
        
        repr_str = repr(usuario)
        assert 'admin@test.com' in repr_str
        assert 'superadministrador' in repr_str

"""
Tests del Servicio de Autenticación
"""
import pytest
from app import create_app
from app.extensions import db
from app.models.usuario import UsuarioAdministrativo
from app.services.auth_service import AuthService


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
def usuario_prueba(app):
    """Crear usuario de prueba"""
    with app.app_context():
        usuario = UsuarioAdministrativo(
            nombre='Usuario Prueba',
            email='test@example.com',
            password='password123',
            rol='superadministrador',
            activo=True
        )
        db.session.add(usuario)
        db.session.commit()
        # Refrescar para asegurar que está bound to session
        db.session.refresh(usuario)
        yield usuario
        db.session.delete(usuario)
        db.session.commit()


class TestAuthService:
    """Tests del servicio de autenticación"""
    
    def test_authenticate_exitoso(self, app, usuario_prueba):
        """Test de autenticación exitosa"""
        with app.app_context():
            usuario = AuthService.authenticate('test@example.com', 'password123')
            assert usuario is not None
            assert usuario.email == 'test@example.com'
            assert usuario.rol == 'superadministrador'
    
    def test_authenticate_password_incorrecto(self, app, usuario_prueba):
        """Test de autenticación con password incorrecto"""
        with app.app_context():
            usuario = AuthService.authenticate('test@example.com', 'wrongpassword')
            assert usuario is None
    
    def test_authenticate_email_inexistente(self, app, usuario_prueba):
        """Test de autenticación con email inexistente"""
        with app.app_context():
            usuario = AuthService.authenticate('nonexistent@example.com', 'password123')
            assert usuario is None
    
    def test_authenticate_usuario_inactivo(self, app, usuario_prueba):
        """Test de autenticación con usuario inactivo"""
        with app.app_context():
            # Desactivar usuario
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            usuario.activo = False
            db.session.commit()
            
            # Intentar autenticar
            usuario_auth = AuthService.authenticate('test@example.com', 'password123')
            assert usuario_auth is None
    
    def test_login_exitoso(self, app, usuario_prueba):
        """Test de login exitoso"""
        with app.app_context():
            # Recargar usuario desde BD
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            result = AuthService.login(usuario)
            assert result is True
    
    def test_login_usuario_inactivo(self, app, usuario_prueba):
        """Test de login con usuario inactivo"""
        with app.app_context():
            # Desactivar usuario
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            usuario.activo = False
            db.session.commit()
            
            # Recargar usuario
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            result = AuthService.login(usuario)
            assert result is False
    
    def test_verify_password(self, app, usuario_prueba):
        """Test de verificación de password"""
        with app.app_context():
            # Recargar usuario desde BD
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            assert usuario.verify_password('password123') is True
            assert usuario.verify_password('wrongpassword') is False
    
    def test_password_no_legible(self, app, usuario_prueba):
        """Test de que el password no es legible directamente"""
        with app.app_context():
            # Recargar usuario desde BD
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            with pytest.raises(AttributeError):
                _ = usuario.password
    
    def test_is_active(self, app, usuario_prueba):
        """Test de propiedad is_active"""
        with app.app_context():
            # Recargar usuario desde BD
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            assert usuario.is_active is True
            
            # Desactivar
            usuario.activo = False
            db.session.commit()
            
            # Recargar
            usuario = UsuarioAdministrativo.query.filter_by(email='test@example.com').first()
            assert usuario.is_active is False


class TestAuthRoutes:
    """Tests de las rutas de autenticación"""
    
    def test_login_page_get(self, client):
        """Test de acceso a página de login (GET)"""
        response = client.get('/admin/login')
        assert response.status_code == 200
        assert b'Iniciar Sesion' in response.data or b'login' in response.data.lower()
    
    def test_login_exitoso(self, client, usuario_prueba, app):
        """Test de login exitoso"""
        with app.app_context():
            response = client.post('/admin/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            }, follow_redirects=False)
            assert response.status_code == 302  # Redirige al dashboard
    
    def test_login_fallido(self, client, usuario_prueba):
        """Test de login con credenciales incorrectas"""
        response = client.post('/admin/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200  # Se queda en la página de login
        assert b'Credenciales' in response.data or b'invalidas' in response.data
    
    def test_login_campos_vacios(self, client):
        """Test de login con campos vacíos"""
        response = client.post('/admin/login', data={
            'email': '',
            'password': ''
        })
        assert response.status_code == 200
        assert b'Por favor' in response.data or b'email' in response.data
    
    def test_logout(self, client, usuario_prueba, app):
        """Test de logout"""
        with app.app_context():
            # Login primero
            client.post('/admin/login', data={
                'email': 'test@example.com',
                'password': 'password123'
            })
            
            # Logout
            response = client.get('/admin/logout', follow_redirects=False)
            assert response.status_code == 302  # Redirige al login

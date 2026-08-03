"""
Modelo UsuarioAdministrativo

Representa a los usuarios que tienen acceso al panel administrativo del sistema.
Pueden ser superadministradores, administradores o personal de ventas.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db
from .base import BaseModel


class UsuarioAdministrativo(UserMixin, BaseModel):
    """
    Usuario con acceso al panel administrativo.
    
    Roles:
    - superadministrador: Acceso total al sistema (gestión de cobertura, usuarios, etc.)
    - administrador: Gestión de solicitudes y análisis de demanda
    - ventas: Visualización y gestión de solicitudes
    
    Campos de auditoría:
    - Este modelo NO hereda los campos creado_por/actualizado_por de BaseModel
      porque sería una dependencia circular (se referencia a sí mismo)
    - En su lugar, define sus propios campos de auditoría sin FK
    """
    __tablename__ = 'usuarios_administrativos'
    
    # Datos del usuario
    nombre = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    _password_hash = db.Column('password_hash', db.String(256), nullable=False)
    
    # Rol y estado
    rol = db.Column(db.String(20), nullable=False, default='ventas', index=True)
    activo = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    # Control de acceso
    ultimo_acceso = db.Column(db.DateTime, nullable=True)
    
    # Campos de auditoría propios (sin FK para evitar dependencia circular)
    fecha_creacion = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        comment='Timestamp de creación del usuario'
    )
    fecha_modificacion = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False,
        comment='Timestamp de última modificación del usuario'
    )
    
    # Nota: Las relaciones inversas para creado_por/actualizado_por no se definen aquí
    # porque BaseModel es abstracto. Si necesitas obtener el usuario que creó un registro,
    # haz una consulta directa: UsuarioAdministrativo.query.get(registro.creado_por)
    
    # Roles válidos
    ROLES_VALIDOS = ['superadministrador', 'administrador', 'ventas']
    
    def __init__(self, **kwargs):
        """
        Inicializa el usuario.
        
        Si se proporciona 'password' en kwargs, se hashea automáticamente.
        """
        password = kwargs.pop('password', None)
        super().__init__(**kwargs)
        if password:
            self.password = password
    
    @property
    def password(self):
        """
        El password no se puede leer directamente (solo el hash).
        """
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """
        Hashea el password antes de almacenarlo.
        """
        self._password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """
        Verifica si el password proporcionado coincide con el hash almacenado.
        
        Args:
            password: Password en texto plano a verificar
            
        Returns:
            bool: True si el password es correcto, False en caso contrario
        """
        return check_password_hash(self._password_hash, password)
    
    def get_id(self):
        """
        Retorna el identificador del usuario para Flask-Login.
        
        Returns:
            str: ID del usuario como string
        """
        return str(self.id)
    
    @property
    def is_active(self):
        """
        Indica si el usuario está activo (puede hacer login).
        
        Returns:
            bool: True si el usuario está activo, False en caso contrario
        """
        return self.activo
    
    def __repr__(self):
        return f'<UsuarioAdministrativo {self.email} - {self.rol}>'
    
    def to_dict(self):
        """
        Convierte el usuario a diccionario para serialización JSON.
        
        Nota: NO incluye el password_hash por seguridad.
        
        Returns:
            dict: Diccionario con los campos del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }

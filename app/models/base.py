"""
Clase base abstracta para todos los modelos del sistema.

Proporciona campos de auditoría comunes:
- id: Clave primaria autoincremental
- creado_por: FK al usuario que creó el registro (nullable para registros del portal)
- fecha_creacion: Timestamp de creación
- actualizado_por: FK al usuario que actualizó el registro (nullable)
- fecha_modificacion: Timestamp de última modificación
"""
from datetime import datetime, timezone
from app.extensions import db


class BaseModel(db.Model):
    """
    Clase base abstracta con campos de auditoría.
    
    Todos los modelos del sistema deben heredar de esta clase para mantener
    consistencia en los campos de auditoría y trazabilidad.
    
    Campos de auditoría:
    - creado_por: FK a UsuarioAdministrativo (nullable para registros del portal)
    - fecha_creacion: Timestamp de creación (auto-generado)
    - actualizado_por: FK a UsuarioAdministrativo (nullable para registros del portal)
    - fecha_modificacion: Timestamp de última modificación (auto-actualizado)
    
    Manejo de usuarios anónimos:
    - Las solicitudes creadas desde el portal público tendrán creado_por=NULL
    - Las solicitudes creadas/modificadas por administradores tendrán el ID del usuario
    - Esto permite distinguir entre registros del sistema y registros de usuarios
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creado_por = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios_administrativos.id'), 
        nullable=True,
        comment='ID del usuario que creó el registro (NULL si fue creado por el portal público)'
    )
    fecha_creacion = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        comment='Timestamp de creación del registro'
    )
    actualizado_por = db.Column(
        db.Integer, 
        db.ForeignKey('usuarios_administrativos.id'), 
        nullable=True,
        comment='ID del usuario que actualizó el registro (NULL si fue actualizado por el portal público)'
    )
    fecha_modificacion = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False,
        comment='Timestamp de última modificación del registro'
    )
    
    # Relaciones con usuario que creó/modificó (opcionales)
    # Se definirán en cada modelo concreto para evitar dependencias circulares
    # creador = db.relationship('UsuarioAdministrativo', foreign_keys=[creado_por])
    # actualizador = db.relationship('UsuarioAdministrativo', foreign_keys=[actualizado_por])
    
    def to_dict(self):
        """
        Convierte el modelo a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos del modelo
        """
        return {
            'id': self.id,
            'creado_por': self.creado_por,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_por': self.actualizado_por,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }

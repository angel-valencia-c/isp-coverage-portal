"""
Modelo NotaSolicitud

Representa una nota interna agregada a una solicitud por un usuario administrativo.
"""
from app.extensions import db
from .base import BaseModel


class NotaSolicitud(BaseModel):
    """
    Nota interna de una solicitud.
    
    Relaciones:
    - Pertenece a una solicitud (N:1)
    - Puede ser creada por un usuario administrativo (N:1, opcional)
    
    Campos:
    - solicitud_id: FK a SolicitudInstalacion
    - texto: Contenido de la nota
    """
    __tablename__ = 'notas_solicitudes'
    
    solicitud_id = db.Column(
        db.Integer, 
        db.ForeignKey('solicitudes_instalacion.id'), 
        nullable=False, 
        index=True,
        comment='ID de la solicitud'
    )
    texto = db.Column(
        db.Text, 
        nullable=False,
        comment='Contenido de la nota'
    )
    
    # Relación con el usuario que creó la nota
    usuario = db.relationship('UsuarioAdministrativo', foreign_keys='NotaSolicitud.creado_por')
    
    def __repr__(self):
        return f'<NotaSolicitud {self.id} - Solicitud {self.solicitud_id}>'
    
    def to_dict(self):
        """
        Convierte la nota a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la nota
        """
        return {
            **super().to_dict(),
            'solicitud_id': self.solicitud_id,
            'texto': self.texto
        }

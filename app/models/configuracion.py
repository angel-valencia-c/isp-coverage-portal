"""
Modelo Configuracion

Representa configuraciones globales del sistema.
"""
from app.extensions import db
from .base import BaseModel


class Configuracion(BaseModel):
    """
    Configuración global del sistema.
    
    Campos:
    - clave: Clave única de la configuración
    - valor: Valor de la configuración (almacenado como string)
    - descripcion: Descripción opcional de la configuración
    """
    __tablename__ = 'configuraciones'
    
    clave = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
        index=True,
        comment='Clave única de la configuración'
    )
    valor = db.Column(
        db.Text,
        nullable=False,
        comment='Valor de la configuración'
    )
    descripcion = db.Column(
        db.Text,
        nullable=True,
        comment='Descripción opcional de la configuración'
    )
    
    def __repr__(self):
        return f'<Configuracion {self.clave}={self.valor}>'
    
    def to_dict(self):
        """
        Convierte la configuración a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la configuración
        """
        return {
            **super().to_dict(),
            'clave': self.clave,
            'valor': self.valor,
            'descripcion': self.descripcion
        }

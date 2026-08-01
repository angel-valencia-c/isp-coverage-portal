"""
Modelo Plan

Representa un plan de servicio de internet ofrecido por Enlaces Costa Grande.
"""
from app.extensions import db
from .base import BaseModel


class Plan(BaseModel):
    """
    Plan de servicio de internet.
    
    Relaciones:
    - Puede estar disponible en muchas coberturas (N:M a través de DisponibilidadPlanZona)
    - Puede tener muchas solicitudes de instalación (1:N)
    
    Campos:
    - nombre: Nombre del plan
    - velocidad_descarga: Velocidad de descarga en Mbps
    - velocidad_subida: Velocidad de subida en Mbps
    - precio_mensual: Precio mensual del plan
    - descripcion: Descripción del plan
    - activo: Si el plan está activo
    - orden: Orden de presentación en el portal
    - destacado: Si el plan está destacado
    """
    __tablename__ = 'planes'
    
    nombre = db.Column(
        db.String(100), 
        nullable=False, 
        unique=True, 
        index=True,
        comment='Nombre del plan'
    )
    velocidad_descarga = db.Column(
        db.Integer, 
        nullable=False,
        comment='Velocidad de descarga en Mbps'
    )
    velocidad_subida = db.Column(
        db.Integer, 
        nullable=False,
        comment='Velocidad de subida en Mbps'
    )
    precio_mensual = db.Column(
        db.Numeric(10, 2), 
        nullable=False,
        comment='Precio mensual del plan'
    )
    descripcion = db.Column(
        db.Text, 
        nullable=True,
        comment='Descripción del plan'
    )
    activo = db.Column(
        db.Boolean, 
        default=True, 
        nullable=False, 
        index=True,
        comment='Indica si el plan está activo'
    )
    orden = db.Column(
        db.Integer, 
        default=0, 
        nullable=False,
        comment='Orden de presentación en el portal'
    )
    destacado = db.Column(
        db.Boolean, 
        default=False, 
        nullable=False,
        comment='Indica si el plan está destacado'
    )
    
    # Relaciones
    disponibilidades = db.relationship(
        'DisponibilidadPlanZona',
        backref='plan',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Plan {self.nombre} ({self.velocidad_descarga}Mbps)>'
    
    def to_dict(self):
        """
        Convierte el plan a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos del plan
        """
        return {
            **super().to_dict(),
            'nombre': self.nombre,
            'velocidad_descarga': self.velocidad_descarga,
            'velocidad_subida': self.velocidad_subida,
            'precio_mensual': float(self.precio_mensual) if self.precio_mensual else None,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'orden': self.orden,
            'destacado': self.destacado
        }

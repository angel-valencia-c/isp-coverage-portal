"""
Modelo Cobertura

Representa la cobertura de servicio en una colonia/comunidad.
Es una relación 1:1 con ColoniaComunidad.
"""
from app.extensions import db
from .base import BaseModel


class Cobertura(BaseModel):
    """
    Cobertura de servicio en una colonia/comunidad.
    
    Relaciones:
    - Pertenece a una colonia/comunidad (1:1)
    - Puede tener muchos planes disponibles (1:N a través de DisponibilidadPlanZona)
    
    Campos:
    - colonia_id: FK a ColoniaComunidad (único, relación 1:1)
    - activa: Si la cobertura está activa
    - tipo_cobertura: Tipo de cobertura (total, parcial, condicional, planificada)
    - fecha_activacion: Fecha de activación
    - fecha_desactivacion: Fecha de desactivación (nullable)
    - notas: Notas adicionales
    - reglas: Campo JSON para reglas futuras
    """
    __tablename__ = 'coberturas'
    
    colonia_id = db.Column(
        db.Integer, 
        db.ForeignKey('colonias_comunidades.id'), 
        nullable=False, 
        unique=True, 
        index=True,
        comment='ID de la colonia/comunidad (relación 1:1)'
    )
    activa = db.Column(
        db.Boolean, 
        default=True, 
        nullable=False, 
        index=True,
        comment='Indica si la cobertura está activa'
    )
    tipo_cobertura = db.Column(
        db.String(20), 
        nullable=False, 
        default='total',
        index=True,
        comment='Tipo de cobertura: total, parcial, condicional, planificada'
    )
    fecha_activacion = db.Column(
        db.DateTime, 
        nullable=True,
        comment='Fecha de activación de la cobertura'
    )
    fecha_desactivacion = db.Column(
        db.DateTime, 
        nullable=True,
        comment='Fecha de desactivación de la cobertura'
    )
    notas = db.Column(
        db.Text, 
        nullable=True,
        comment='Notas adicionales sobre la cobertura'
    )
    reglas = db.Column(
        db.JSON, 
        nullable=True,
        comment='Campo JSON para reglas futuras de cobertura'
    )
    
    # Relaciones
    planes_disponibles = db.relationship(
        'DisponibilidadPlanZona',
        backref='cobertura',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Tipos válidos
    TIPOS_VALIDOS = ['total', 'parcial', 'condicional', 'planificada']
    
    def __repr__(self):
        return f'<Cobertura colonia_id={self.colonia_id} ({self.tipo_cobertura})>'
    
    def to_dict(self):
        """
        Convierte la cobertura a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la cobertura
        """
        return {
            **super().to_dict(),
            'colonia_id': self.colonia_id,
            'activa': self.activa,
            'tipo_cobertura': self.tipo_cobertura,
            'fecha_activacion': self.fecha_activacion.isoformat() if self.fecha_activacion else None,
            'fecha_desactivacion': self.fecha_desactivacion.isoformat() if self.fecha_desactivacion else None,
            'notas': self.notas,
            'reglas': self.reglas
        }

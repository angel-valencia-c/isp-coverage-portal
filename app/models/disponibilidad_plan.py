"""
Modelo DisponibilidadPlanZona

Tabla intermedia que representa la disponibilidad de un plan en una cobertura específica.
Es una relación N:M entre Cobertura y Plan.
"""
from app.extensions import db
from .base import BaseModel


class DisponibilidadPlanZona(BaseModel):
    """
    Disponibilidad de un plan en una cobertura específica.
    
    Relaciones:
    - Pertenece a una cobertura (N:1)
    - Pertenece a un plan (N:1)
    
    Campos:
    - cobertura_id: FK a Cobertura
    - plan_id: FK a Plan
    - costo_instalacion: Costo de instalación para esta zona (puede variar)
    - disponible: Si el plan está disponible en esta zona
    """
    __tablename__ = 'disponibilidad_planes_zona'
    
    cobertura_id = db.Column(
        db.Integer, 
        db.ForeignKey('coberturas.id'), 
        nullable=False, 
        index=True,
        comment='ID de la cobertura'
    )
    plan_id = db.Column(
        db.Integer, 
        db.ForeignKey('planes.id'), 
        nullable=False, 
        index=True,
        comment='ID del plan'
    )
    costo_instalacion = db.Column(
        db.Numeric(10, 2), 
        nullable=True,
        comment='Costo de instalación para esta zona (puede variar por zona)'
    )
    disponible = db.Column(
        db.Boolean, 
        default=True, 
        nullable=False,
        comment='Indica si el plan está disponible en esta zona'
    )
    
    # Constraint único compuesto (cobertura + plan)
    __table_args__ = (
        db.UniqueConstraint('cobertura_id', 'plan_id', name='uq_cobertura_plan'),
    )
    
    def __repr__(self):
        return f'<DisponibilidadPlanZona cobertura={self.cobertura_id} plan={self.plan_id}>'
    
    def to_dict(self):
        """
        Convierte la disponibilidad a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la disponibilidad
        """
        return {
            **super().to_dict(),
            'cobertura_id': self.cobertura_id,
            'plan_id': self.plan_id,
            'costo_instalacion': float(self.costo_instalacion) if self.costo_instalacion else None,
            'disponible': self.disponible
        }

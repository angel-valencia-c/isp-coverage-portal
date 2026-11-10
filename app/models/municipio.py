"""
Modelo Municipio

Representa un municipio del estado de Guerrero donde opera Internet Regional.
Es la unidad geográfica de nivel superior en la jerarquía territorial.
"""
from app.extensions import db
from .base import BaseModel


class Municipio(BaseModel):
    """
    Municipio del estado de Guerrero.
    
    Relaciones:
    - Un municipio tiene muchas colonias/comunidades (1:N)
    - Un municipio puede tener muchas solicitudes de instalación (1:N)
    
    Campos:
    - nombre: Nombre del municipio (único)
    - estado: Estado de la república (default: 'Guerrero')
    - activo: Si el municipio está activo en el sistema
    """
    __tablename__ = 'municipios'
    
    nombre = db.Column(
        db.String(100), 
        nullable=False, 
        unique=True, 
        index=True,
        comment='Nombre del municipio'
    )
    estado = db.Column(
        db.String(50), 
        nullable=False, 
        default='Guerrero',
        comment='Estado de la república mexicana'
    )
    activo = db.Column(
        db.Boolean, 
        default=True, 
        nullable=False, 
        index=True,
        comment='Indica si el municipio está activo en el sistema'
    )
    
    # Relaciones
    colonias = db.relationship(
        'ColoniaComunidad',
        backref='municipio',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Municipio {self.nombre}, {self.estado}>'
    
    def to_dict(self):
        """
        Convierte el municipio a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos del municipio
        """
        return {
            **super().to_dict(),
            'nombre': self.nombre,
            'estado': self.estado,
            'activo': self.activo
        }

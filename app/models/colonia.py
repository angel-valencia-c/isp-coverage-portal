"""
Modelo ColoniaComunidad

Representa una colonia o comunidad dentro de un municipio.
Es la unidad geográfica de nivel inferior en la jerarquía territorial V1.
"""
from app.extensions import db
from .base import BaseModel


class ColoniaComunidad(BaseModel):
    """
    Colonia o comunidad dentro de un municipio.
    
    Relaciones:
    - Pertenece a un municipio (N:1)
    - Puede tener una cobertura (1:1, opcional)
    - Puede tener muchas solicitudes de instalación (1:N)
    
    Campos:
    - nombre: Nombre de la colonia/comunidad
    - tipo: Tipo de asentamiento (colonia, comunidad, ranchería, otra)
    - municipio_id: FK al municipio
    - activo: Si la colonia está activa en el sistema
    """
    __tablename__ = 'colonias_comunidades'
    
    nombre = db.Column(
        db.String(150), 
        nullable=False, 
        index=True,
        comment='Nombre de la colonia o comunidad'
    )
    tipo = db.Column(
        db.String(20), 
        nullable=False, 
        default='colonia',
        index=True,
        comment='Tipo de asentamiento: colonia, comunidad, ranchería, otra'
    )
    municipio_id = db.Column(
        db.Integer, 
        db.ForeignKey('municipios.id'), 
        nullable=False, 
        index=True,
        comment='ID del municipio al que pertenece'
    )
    activo = db.Column(
        db.Boolean, 
        default=True, 
        nullable=False, 
        index=True,
        comment='Indica si la colonia está activa en el sistema'
    )
    
    # Relaciones
    cobertura = db.relationship(
        'Cobertura',
        backref='colonia',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    # Tipos válidos
    TIPOS_VALIDOS = ['colonia', 'comunidad', 'ranchería', 'otra']
    
    # Constraint único compuesto (nombre + municipio)
    __table_args__ = (
        db.UniqueConstraint('nombre', 'municipio_id', name='uq_colonia_municipio'),
    )
    
    def __repr__(self):
        return f'<ColoniaComunidad {self.nombre} ({self.tipo})>'
    
    def to_dict(self):
        """
        Convierte la colonia a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la colonia
        """
        return {
            **super().to_dict(),
            'nombre': self.nombre,
            'tipo': self.tipo,
            'municipio_id': self.municipio_id,
            'activo': self.activo
        }

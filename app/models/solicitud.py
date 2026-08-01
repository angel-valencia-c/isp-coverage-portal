"""
Modelo SolicitudInstalacion

Representa una solicitud de instalación de servicio de internet.
Puede ser una solicitud con cobertura o un lead sin cobertura.
"""
from app.extensions import db
from .base import BaseModel


class SolicitudInstalacion(BaseModel):
    """
    Solicitud de instalación de servicio de internet.
    
    Tipos:
    - solicitud_cobertura: Prospecto con cobertura disponible
    - lead_sin_cobertura: Prospecto sin cobertura (lead para expansión)
    
    Relaciones:
    - Pertenece a un municipio (N:1)
    - Pertenece a una colonia/comunidad (N:1)
    - Puede tener un plan (N:1, nullable para leads sin cobertura)
    - Puede tener muchas notas (1:N)
    - Puede estar marcada como duplicada de otra solicitud (self-referential)
    
    Campos:
    - nombre_prospecto: Nombre del prospecto
    - telefono_contacto: Teléfono de contacto (10 dígitos)
    - direccion_especifica: Dirección específica
    - municipio_id: FK a Municipio
    - colonia_id: FK a ColoniaComunidad
    - plan_id: FK a Plan (nullable para leads sin cobertura)
    - costo_instalacion_cotizado: Costo de instalación cotizado
    - precio_mensual_cotizado: Precio mensual cotizado
    - estado: Estado de la solicitud
    - origen: Origen de la solicitud
    - tipo: Tipo de solicitud
    - solicitud_duplicada_de: FK a otra solicitud (nullable)
    """
    __tablename__ = 'solicitudes_instalacion'
    
    # Datos del prospecto
    nombre_prospecto = db.Column(
        db.String(200), 
        nullable=False, 
        index=True,
        comment='Nombre completo del prospecto'
    )
    telefono_contacto = db.Column(
        db.String(10), 
        nullable=False, 
        index=True,
        comment='Teléfono de contacto (10 dígitos)'
    )
    direccion_especifica = db.Column(
        db.Text, 
        nullable=True,
        comment='Dirección específica del prospecto'
    )
    
    # Ubicación
    municipio_id = db.Column(
        db.Integer, 
        db.ForeignKey('municipios.id'), 
        nullable=False, 
        index=True,
        comment='ID del municipio'
    )
    colonia_id = db.Column(
        db.Integer, 
        db.ForeignKey('colonias_comunidades.id'), 
        nullable=False, 
        index=True,
        comment='ID de la colonia/comunidad'
    )
    
    # Plan y cotización
    plan_id = db.Column(
        db.Integer, 
        db.ForeignKey('planes.id'), 
        nullable=True, 
        index=True,
        comment='ID del plan (nullable para leads sin cobertura)'
    )
    costo_instalacion_cotizado = db.Column(
        db.Numeric(10, 2), 
        nullable=True,
        comment='Costo de instalación cotizado'
    )
    precio_mensual_cotizado = db.Column(
        db.Numeric(10, 2), 
        nullable=True,
        comment='Precio mensual cotizado'
    )
    
    # Estado y seguimiento
    estado = db.Column(
        db.String(20), 
        nullable=False, 
        default='pendiente',
        index=True,
        comment='Estado de la solicitud: pendiente, contactado, agendado, cancelado, duplicado'
    )
    origen = db.Column(
        db.String(20), 
        nullable=False, 
        default='portal',
        index=True,
        comment='Origen de la solicitud: portal, telefono, whatsapp, presencial, otro'
    )
    tipo = db.Column(
        db.String(30), 
        nullable=False, 
        default='solicitud_cobertura',
        index=True,
        comment='Tipo: solicitud_cobertura o lead_sin_cobertura'
    )
    
    # Duplicados
    solicitud_duplicada_de = db.Column(
        db.Integer, 
        db.ForeignKey('solicitudes_instalacion.id'), 
        nullable=True,
        comment='ID de la solicitud original si esta es duplicada'
    )
    
    # Relaciones
    municipio = db.relationship('Municipio', backref='solicitudes')
    colonia = db.relationship('ColoniaComunidad', backref='solicitudes')
    plan = db.relationship('Plan', backref='solicitudes')
    notas = db.relationship(
        'NotaSolicitud',
        backref='solicitud',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    duplicada_de = db.relationship(
        'SolicitudInstalacion',
        remote_side='SolicitudInstalacion.id',
        backref='duplicadas'
    )
    
    # Índices compuestos para consultas frecuentes
    __table_args__ = (
        db.Index('idx_solicitud_estado_fecha', 'estado', 'fecha_creacion'),
        db.Index('idx_solicitud_municipio_colonia', 'municipio_id', 'colonia_id'),
    )
    
    # Validaciones de estado
    ESTADOS_VALIDOS = ['pendiente', 'contactado', 'agendado', 'cancelado', 'duplicado']
    ORIGENES_VALIDOS = ['portal', 'telefono', 'whatsapp', 'presencial', 'otro']
    TIPOS_VALIDOS = ['solicitud_cobertura', 'lead_sin_cobertura']
    
    def __repr__(self):
        return f'<SolicitudInstalacion {self.id} - {self.nombre_prospecto} ({self.estado})>'
    
    def to_dict(self):
        """
        Convierte la solicitud a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los campos de la solicitud
        """
        return {
            **super().to_dict(),
            'nombre_prospecto': self.nombre_prospecto,
            'telefono_contacto': self.telefono_contacto,
            'direccion_especifica': self.direccion_especifica,
            'municipio_id': self.municipio_id,
            'colonia_id': self.colonia_id,
            'plan_id': self.plan_id,
            'costo_instalacion_cotizado': float(self.costo_instalacion_cotizado) if self.costo_instalacion_cotizado else None,
            'precio_mensual_cotizado': float(self.precio_mensual_cotizado) if self.precio_mensual_cotizado else None,
            'estado': self.estado,
            'origen': self.origen,
            'tipo': self.tipo,
            'solicitud_duplicada_de': self.solicitud_duplicada_de
        }

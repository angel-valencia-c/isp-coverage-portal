"""
Modelos SQLAlchemy

Este módulo contiene todos los modelos de la base de datos.
Todos los modelos heredan de BaseModel para mantener consistencia
en los campos de auditoría.
"""
from .base import BaseModel
from .usuario import UsuarioAdministrativo
from .municipio import Municipio
from .colonia import ColoniaComunidad
from .cobertura import Cobertura
from .plan import Plan
from .disponibilidad_plan import DisponibilidadPlanZona
from .solicitud import SolicitudInstalacion
from .nota_solicitud import NotaSolicitud
from .configuracion import Configuracion

__all__ = [
    'BaseModel',
    'UsuarioAdministrativo',
    'Municipio',
    'ColoniaComunidad',
    'Cobertura',
    'Plan',
    'DisponibilidadPlanZona',
    'SolicitudInstalacion',
    'NotaSolicitud',
    'Configuracion',
]

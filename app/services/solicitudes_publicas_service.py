"""
Servicio de Solicitudes Públicas

Maneja la lógica de negocio para el formulario de solicitud en el portal público:
- Crear solicitud de instalación
- Validar duplicados
- Validar campos
- Crear lead sin cobertura
"""
from datetime import datetime, timedelta
from app.extensions import db
from app.models.solicitud import SolicitudInstalacion
from app.models.colonia import ColoniaComunidad
from app.models.plan import Plan


class SolicitudesPublicasService:
    """
    Servicio para solicitudes en el portal público.
    """
    
    @staticmethod
    def crear_solicitud(nombre_prospecto, telefono_contacto, direccion_especifica,
                       municipio_id, colonia_id, plan_id=None, 
                       costo_instalacion_cotizado=None, precio_mensual_cotizado=None):
        """
        Crea una nueva solicitud de instalación.
        
        Args:
            nombre_prospecto: Nombre completo del prospecto
            telefono_contacto: Teléfono de contacto (10 dígitos)
            direccion_especifica: Dirección específica
            municipio_id: ID del municipio
            colonia_id: ID de la colonia
            plan_id: ID del plan (opcional para leads sin cobertura)
            costo_instalacion_cotizado: Costo de instalación cotizado
            precio_mensual_cotizado: Precio mensual cotizado
            
        Returns:
            SolicitudInstalacion: Solicitud creada
            
        Raises:
            ValueError: Si hay errores de validación
        """
        # Validar campos obligatorios
        if not nombre_prospecto or not nombre_prospecto.strip():
            raise ValueError('El nombre es obligatorio')
        
        if not telefono_contacto or not telefono_contacto.strip():
            raise ValueError('El teléfono es obligatorio')
        
        # Validar formato de teléfono (10 dígitos)
        telefono_limpio = ''.join(filter(str.isdigit, telefono_contacto))
        if len(telefono_limpio) != 10:
            raise ValueError('El teléfono debe tener 10 dígitos')
        
        if not direccion_especifica or not direccion_especifica.strip():
            raise ValueError('La dirección es obligatoria')
        
        if not municipio_id:
            raise ValueError('El municipio es obligatorio')
        
        if not colonia_id:
            raise ValueError('La colonia es obligatoria')
        
        # Validar que la colonia existe
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError('La colonia seleccionada no es válida')
        
        # Validar que el municipio de la colonia coincide
        if colonia.municipio_id != municipio_id:
            raise ValueError('La colonia no pertenece al municipio seleccionado')
        
        # Validar plan si se proporciona
        if plan_id:
            plan = Plan.query.get(plan_id)
            if not plan:
                raise ValueError('El plan seleccionado no es válido')
        
        # Verificar duplicados (mismo teléfono en últimos 7 días)
        fecha_limite = datetime.utcnow() - timedelta(days=7)
        solicitud_existente = SolicitudInstalacion.query.filter(
            SolicitudInstalacion.telefono_contacto == telefono_limpio,
            SolicitudInstalacion.fecha_creacion >= fecha_limite,
            SolicitudInstalacion.estado.in_(['pendiente', 'contactado', 'agendado'])
        ).first()
        
        if solicitud_existente:
            raise ValueError('Ya existe una solicitud pendiente con este teléfono. Te contactaremos pronto.')
        
        # Determinar tipo de solicitud
        tipo = 'solicitud_cobertura' if plan_id else 'lead_sin_cobertura'
        
        # Crear solicitud
        solicitud = SolicitudInstalacion(
            nombre_prospecto=nombre_prospecto.strip(),
            telefono_contacto=telefono_limpio,
            direccion_especifica=direccion_especifica.strip(),
            municipio_id=municipio_id,
            colonia_id=colonia_id,
            plan_id=plan_id,
            costo_instalacion_cotizado=costo_instalacion_cotizado,
            precio_mensual_cotizado=precio_mensual_cotizado,
            estado='pendiente',
            origen='portal',
            tipo=tipo
        )
        
        db.session.add(solicitud)
        db.session.commit()
        
        return solicitud
    
    @staticmethod
    def crear_lead_sin_cobertura(nombre_prospecto, telefono_contacto, 
                                 municipio_id, colonia_id, direccion_especifica=None):
        """
        Crea un lead sin cobertura (prospecto interesado en zona sin cobertura).
        
        Args:
            nombre_prospecto: Nombre completo del prospecto
            telefono_contacto: Teléfono de contacto (10 dígitos)
            municipio_id: ID del municipio
            colonia_id: ID de la colonia
            direccion_especifica: Dirección específica (opcional para leads)
            
        Returns:
            SolicitudInstalacion: Lead creado
            
        Raises:
            ValueError: Si hay errores de validación
        """
        return SolicitudesPublicasService.crear_solicitud(
            nombre_prospecto=nombre_prospecto,
            telefono_contacto=telefono_contacto,
            direccion_especifica=direccion_especifica or 'No especificada',
            municipio_id=municipio_id,
            colonia_id=colonia_id,
            plan_id=None,
            costo_instalacion_cotizado=None,
            precio_mensual_cotizado=None
        )
    
    @staticmethod
    def verificar_duplicado(telefono_contacto):
        """
        Verifica si existe una solicitud duplicada con el mismo teléfono.
        
        Args:
            telefono_contacto: Teléfono de contacto
            
        Returns:
            bool: True si existe duplicado, False en caso contrario
        """
        telefono_limpio = ''.join(filter(str.isdigit, telefono_contacto))
        fecha_limite = datetime.utcnow() - timedelta(days=7)
        
        solicitud_existente = SolicitudInstalacion.query.filter(
            SolicitudInstalacion.telefono_contacto == telefono_limpio,
            SolicitudInstalacion.fecha_creacion >= fecha_limite,
            SolicitudInstalacion.estado.in_(['pendiente', 'contactado', 'agendado'])
        ).first()
        
        return solicitud_existente is not None

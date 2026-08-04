"""
Servicio de Disponibilidad de Planes por Zona

Maneja la lógica de negocio para la asociación de planes a zonas de cobertura:
- Asociar planes a coberturas
- Configurar costos de instalación por zona/plan
- Configurar costo estándar base global
- Validaciones de negocio
- Campos de auditoría
"""
from decimal import Decimal
from app.extensions import db
from app.models.disponibilidad_plan import DisponibilidadPlanZona
from app.models.cobertura import Cobertura
from app.models.plan import Plan


class DisponibilidadPlanService:
    """
    Servicio para gestión de disponibilidad de planes por zona.
    """
    
    @staticmethod
    def create(cobertura_id, plan_id, costo_instalacion=None, usuario_id=None):
        """
        Asocia un plan a una cobertura.
        
        Args:
            cobertura_id: ID de la cobertura
            plan_id: ID del plan
            costo_instalacion: Costo de instalación para esta zona (opcional)
            usuario_id: ID del usuario que crea el registro
            
        Returns:
            DisponibilidadPlanZona: Disponibilidad creada
            
        Raises:
            ValueError: Si la cobertura o plan no existen, o si ya existe la asociación
        """
        # Validar que la cobertura existe
        cobertura = Cobertura.query.get(cobertura_id)
        if not cobertura:
            raise ValueError(f'No existe una cobertura con ID: {cobertura_id}')
        
        # Validar que el plan existe
        plan = Plan.query.get(plan_id)
        if not plan:
            raise ValueError(f'No existe un plan con ID: {plan_id}')
        
        # Validar que no exista ya la asociación
        existente = DisponibilidadPlanZona.query.filter_by(
            cobertura_id=cobertura_id,
            plan_id=plan_id
        ).first()
        if existente:
            raise ValueError(f'El plan "{plan.nombre}" ya está asociado a esta cobertura')
        
        # Crear disponibilidad
        disponibilidad = DisponibilidadPlanZona(
            cobertura_id=cobertura_id,
            plan_id=plan_id,
            costo_instalacion=Decimal(str(costo_instalacion)) if costo_instalacion else None,
            creado_por=usuario_id
        )
        
        db.session.add(disponibilidad)
        db.session.commit()
        
        return disponibilidad
    
    @staticmethod
    def get_by_cobertura(cobertura_id):
        """
        Obtiene todos los planes disponibles en una cobertura.
        
        Args:
            cobertura_id: ID de la cobertura
            
        Returns:
            list: Lista de disponibilidades con información del plan
        """
        disponibilidades = DisponibilidadPlanZona.query.filter_by(
            cobertura_id=cobertura_id
        ).all()
        
        resultado = []
        for disp in disponibilidades:
            resultado.append({
                'disponibilidad': disp,
                'plan': disp.plan
            })
        
        return resultado
    
    @staticmethod
    def get_by_id(disponibilidad_id):
        """
        Obtiene una disponibilidad por ID.
        
        Args:
            disponibilidad_id: ID de la disponibilidad
            
        Returns:
            DisponibilidadPlanZona: Disponibilidad si existe, None en caso contrario
        """
        return DisponibilidadPlanZona.query.get(disponibilidad_id)
    
    @staticmethod
    def update_costo(disponibilidad_id, costo_instalacion, usuario_id=None):
        """
        Actualiza el costo de instalación de una disponibilidad.
        
        Args:
            disponibilidad_id: ID de la disponibilidad
            costo_instalacion: Nuevo costo de instalación
            usuario_id: ID del usuario que actualiza
            
        Returns:
            DisponibilidadPlanZona: Disponibilidad actualizada
            
        Raises:
            ValueError: Si la disponibilidad no existe
        """
        disponibilidad = DisponibilidadPlanZona.query.get(disponibilidad_id)
        if not disponibilidad:
            raise ValueError(f'No existe una disponibilidad con ID: {disponibilidad_id}')
        
        disponibilidad.costo_instalacion = Decimal(str(costo_instalacion)) if costo_instalacion else None
        disponibilidad.actualizado_por = usuario_id
        
        db.session.commit()
        
        return disponibilidad
    
    @staticmethod
    def remove(disponibilidad_id, usuario_id=None):
        """
        Elimina una asociación plan-cobertura.
        
        Args:
            disponibilidad_id: ID de la disponibilidad
            usuario_id: ID del usuario que elimina
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si la disponibilidad no existe
        """
        disponibilidad = DisponibilidadPlanZona.query.get(disponibilidad_id)
        if not disponibilidad:
            raise ValueError(f'No existe una disponibilidad con ID: {disponibilidad_id}')
        
        db.session.delete(disponibilidad)
        db.session.commit()
        
        return True
    
    @staticmethod
    def get_planes_disponibles_para_asociar(cobertura_id):
        """
        Obtiene los planes que aún no están asociados a una cobertura.
        
        Args:
            cobertura_id: ID de la cobertura
            
        Returns:
            list: Lista de planes disponibles para asociar
        """
        # Obtener IDs de planes ya asociados
        planes_asociados = db.session.query(DisponibilidadPlanZona.plan_id).filter_by(
            cobertura_id=cobertura_id
        ).all()
        planes_asociados_ids = [p[0] for p in planes_asociados]
        
        # Obtener planes activos que no están asociados
        planes_disponibles = Plan.query.filter(
            Plan.activo == True,
            ~Plan.id.in_(planes_asociados_ids)
        ).order_by(Plan.orden, Plan.nombre).all()
        
        return planes_disponibles
    
    @staticmethod
    def get_costo_estandar_base():
        """
        Obtiene el costo estándar base de instalación.
        
        Returns:
            Decimal: Costo estándar base, o None si no está configurado
        """
        # En V1, el costo estándar base se almacena como una configuración global
        # Por ahora, lo obtenemos de una tabla de configuración o lo hardcodeamos
        # En futuras versiones, esto debería estar en una tabla de configuración
        from app.models.configuracion import Configuracion
        config = Configuracion.query.filter_by(clave='costo_estandar_base').first()
        if config:
            return Decimal(config.valor)
        return None
    
    @staticmethod
    def set_costo_estandar_base(costo, usuario_id=None):
        """
        Configura el costo estándar base de instalación.
        
        Args:
            costo: Costo estándar base
            usuario_id: ID del usuario que configura
            
        Returns:
            bool: True si se configuró correctamente
        """
        from app.models.configuracion import Configuracion
        
        config = Configuracion.query.filter_by(clave='costo_estandar_base').first()
        if config:
            config.valor = str(costo)
            config.actualizado_por = usuario_id
        else:
            config = Configuracion(
                clave='costo_estandar_base',
                valor=str(costo),
                creado_por=usuario_id
            )
            db.session.add(config)
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_coberturas_sin_planes():
        """
        Obtiene las coberturas que no tienen planes asociados.
        
        Returns:
            list: Lista de coberturas sin planes
        """
        # Obtener IDs de coberturas con planes asociados
        coberturas_con_planes = db.session.query(
            DisponibilidadPlanZona.cobertura_id
        ).distinct().all()
        coberturas_con_planes_ids = [c[0] for c in coberturas_con_planes]
        
        # Obtener coberturas activas sin planes asociados
        coberturas_sin_planes = Cobertura.query.filter(
            Cobertura.activa == True,
            ~Cobertura.id.in_(coberturas_con_planes_ids)
        ).all()
        
        return coberturas_sin_planes

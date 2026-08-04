"""
Servicio de Planes

Maneja la lógica de negocio para la gestión de planes de internet:
- Crear, leer, actualizar y desactivar planes
- Validaciones de negocio
- Campos de auditoría
"""
from app.extensions import db
from app.models.plan import Plan


class PlanService:
    """
    Servicio para gestión de planes de internet.
    """
    
    @staticmethod
    def create(nombre, velocidad_descarga, velocidad_subida, precio_mensual, 
               descripcion=None, orden=0, destacado=False, usuario_id=None):
        """
        Crea un nuevo plan de internet.
        
        Args:
            nombre: Nombre del plan
            velocidad_descarga: Velocidad de descarga en Mbps
            velocidad_subida: Velocidad de subida en Mbps
            precio_mensual: Precio mensual del plan
            descripcion: Descripción del plan (opcional)
            orden: Orden de visualización (default: 0)
            destacado: Si el plan es destacado (default: False)
            usuario_id: ID del usuario que crea el registro
            
        Returns:
            Plan: Plan creado
            
        Raises:
            ValueError: Si ya existe un plan con el mismo nombre
        """
        # Validar duplicados
        existente = Plan.query.filter_by(nombre=nombre).first()
        if existente:
            raise ValueError(f'Ya existe un plan con el nombre: {nombre}')
        
        # Crear plan
        plan = Plan(
            nombre=nombre,
            velocidad_descarga=velocidad_descarga,
            velocidad_subida=velocidad_subida,
            precio_mensual=precio_mensual,
            descripcion=descripcion,
            orden=orden,
            destacado=destacado,
            activo=True,
            creado_por=usuario_id
        )
        
        db.session.add(plan)
        db.session.commit()
        
        return plan
    
    @staticmethod
    def get_all(incluir_inactivos=False):
        """
        Obtiene todos los planes.
        
        Args:
            incluir_inactivos: Si True, incluye planes inactivos
            
        Returns:
            list: Lista de planes ordenados por orden y nombre
        """
        query = Plan.query
        
        if not incluir_inactivos:
            query = query.filter_by(activo=True)
        
        return query.order_by(Plan.orden, Plan.nombre).all()
    
    @staticmethod
    def get_by_id(plan_id):
        """
        Obtiene un plan por ID.
        
        Args:
            plan_id: ID del plan
            
        Returns:
            Plan: Plan si existe, None en caso contrario
        """
        return Plan.query.get(plan_id)
    
    @staticmethod
    def update(plan_id, nombre=None, velocidad_descarga=None, velocidad_subida=None,
               precio_mensual=None, descripcion=None, orden=None, destacado=None, 
               usuario_id=None):
        """
        Actualiza un plan existente.
        
        Args:
            plan_id: ID del plan a actualizar
            nombre: Nuevo nombre (opcional)
            velocidad_descarga: Nueva velocidad de descarga (opcional)
            velocidad_subida: Nueva velocidad de subida (opcional)
            precio_mensual: Nuevo precio mensual (opcional)
            descripcion: Nueva descripción (opcional)
            orden: Nuevo orden (opcional)
            destacado: Nuevo estado destacado (opcional)
            usuario_id: ID del usuario que actualiza el registro
            
        Returns:
            Plan: Plan actualizado
            
        Raises:
            ValueError: Si el plan no existe o si el nuevo nombre ya existe
        """
        plan = Plan.query.get(plan_id)
        if not plan:
            raise ValueError(f'No existe un plan con ID: {plan_id}')
        
        # Validar duplicados si se cambia el nombre
        if nombre and nombre != plan.nombre:
            existente = Plan.query.filter_by(nombre=nombre).first()
            if existente:
                raise ValueError(f'Ya existe un plan con el nombre: {nombre}')
        
        # Actualizar campos
        if nombre is not None:
            plan.nombre = nombre
        if velocidad_descarga is not None:
            plan.velocidad_descarga = velocidad_descarga
        if velocidad_subida is not None:
            plan.velocidad_subida = velocidad_subida
        if precio_mensual is not None:
            plan.precio_mensual = precio_mensual
        if descripcion is not None:
            plan.descripcion = descripcion
        if orden is not None:
            plan.orden = orden
        if destacado is not None:
            plan.destacado = destacado
        
        plan.actualizado_por = usuario_id
        
        db.session.commit()
        
        return plan
    
    @staticmethod
    def deactivate(plan_id, usuario_id=None):
        """
        Desactiva un plan (no lo elimina).
        
        Args:
            plan_id: ID del plan a desactivar
            usuario_id: ID del usuario que desactiva el registro
            
        Returns:
            Plan: Plan desactivado
            
        Raises:
            ValueError: Si el plan no existe
        """
        plan = Plan.query.get(plan_id)
        if not plan:
            raise ValueError(f'No existe un plan con ID: {plan_id}')
        
        plan.activo = False
        plan.actualizado_por = usuario_id
        
        db.session.commit()
        
        return plan
    
    @staticmethod
    def activate(plan_id, usuario_id=None):
        """
        Activa un plan previamente desactivado.
        
        Args:
            plan_id: ID del plan a activar
            usuario_id: ID del usuario que activa el registro
            
        Returns:
            Plan: Plan activado
            
        Raises:
            ValueError: Si el plan no existe
        """
        plan = Plan.query.get(plan_id)
        if not plan:
            raise ValueError(f'No existe un plan con ID: {plan_id}')
        
        plan.activo = True
        plan.actualizado_por = usuario_id
        
        db.session.commit()
        
        return plan

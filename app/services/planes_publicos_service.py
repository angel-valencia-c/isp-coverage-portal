"""
Servicio de Planes Públicos

Maneja la lógica de negocio para la visualización de planes en el portal público:
- Obtener planes disponibles por cobertura
- Calcular cotización estimada
- Obtener información de planes para visualización
"""
from decimal import Decimal
from app.extensions import db
from app.models.plan import Plan
from app.models.disponibilidad_plan import DisponibilidadPlanZona
from app.models.cobertura import Cobertura
from app.models.configuracion import Configuracion


class PlanesPublicosService:
    """
    Servicio para visualización de planes en el portal público.
    """
    
    @staticmethod
    def get_planes_disponibles(cobertura_id):
        """
        Obtiene los planes disponibles para una cobertura específica.
        
        Args:
            cobertura_id: ID de la cobertura
            
        Returns:
            list: Lista de diccionarios con información de planes disponibles
        """
        disponibilidades = DisponibilidadPlanZona.query.filter_by(
            cobertura_id=cobertura_id
        ).all()
        
        planes_info = []
        for disp in disponibilidades:
            plan = disp.plan
            
            # Obtener costo de instalación
            costo_instalacion = disp.costo_instalacion
            if costo_instalacion is None:
                # Usar costo estándar base si no hay costo personalizado
                costo_instalacion = PlanesPublicosService.get_costo_estandar_base()
            
            planes_info.append({
                'plan': plan,
                'disponibilidad': disp,
                'costo_instalacion': costo_instalacion or Decimal('0'),
                'precio_mensual': plan.precio_mensual
            })
        
        # Ordenar por campo 'orden' y luego por nombre
        planes_info.sort(key=lambda x: (x['plan'].orden, x['plan'].nombre))
        
        return planes_info
    
    @staticmethod
    def get_costo_estandar_base():
        """
        Obtiene el costo estándar base de instalación.
        
        Returns:
            Decimal: Costo estándar base, o 0 si no está configurado
        """
        config = Configuracion.query.filter_by(clave='costo_estandar_base').first()
        if config and config.valor:
            return Decimal(config.valor)
        return Decimal('0')
    
    @staticmethod
    def calcular_cotizacion(plan_id, cobertura_id):
        """
        Calcula la cotización estimada para un plan en una cobertura específica.
        
        Args:
            plan_id: ID del plan
            cobertura_id: ID de la cobertura
            
        Returns:
            dict: Diccionario con información de la cotización
                - plan: Información del plan
                - costo_instalacion: Costo de instalación
                - precio_mensual: Precio mensual
                - total_inicial: Total a pagar inicialmente (instalación + primer mes)
                - mensaje: Mensaje descriptivo
        """
        plan = Plan.query.get(plan_id)
        if not plan:
            return None
        
        # Obtener disponibilidad
        disponibilidad = DisponibilidadPlanZona.query.filter_by(
            plan_id=plan_id,
            cobertura_id=cobertura_id
        ).first()
        
        if not disponibilidad:
            return None
        
        # Obtener costo de instalación
        costo_instalacion = disponibilidad.costo_instalacion
        if costo_instalacion is None:
            costo_instalacion = PlanesPublicosService.get_costo_estandar_base()
        
        precio_mensual = plan.precio_mensual
        total_inicial = costo_instalacion + precio_mensual
        
        return {
            'plan': plan,
            'costo_instalacion': costo_instalacion,
            'precio_mensual': precio_mensual,
            'total_inicial': total_inicial,
            'mensaje': f'Instalación: ${costo_instalacion} + Primer mes: ${precio_mensual}'
        }
    
    @staticmethod
    def get_plan_destacado(planes_info):
        """
        Obtiene el plan destacado de una lista de planes.
        
        Args:
            planes_info: Lista de información de planes
            
        Returns:
            dict: Información del plan destacado, o None si no hay
        """
        for plan_info in planes_info:
            if plan_info['plan'].destacado:
                return plan_info
        return None

"""
Servicio de Dashboard

Maneja la lógica de negocio para el dashboard administrativo:
- Obtener métricas clave del sistema
- Obtener resumen de solicitudes
- Obtener análisis básico por zona
"""
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura
from app.models.plan import Plan
from app.models.solicitud import SolicitudInstalacion
from app.models.disponibilidad_plan import DisponibilidadPlanZona


class DashboardService:
    """
    Servicio para el dashboard administrativo.
    """
    
    @staticmethod
    def get_metricas_generales():
        """
        Obtiene métricas generales del sistema.
        
        Returns:
            dict: Diccionario con métricas clave
        """
        metricas = {
            'total_municipios': Municipio.query.filter_by(activo=True).count(),
            'total_colonias': ColoniaComunidad.query.filter_by(activo=True).count(),
            'total_coberturas_activas': Cobertura.query.filter_by(activa=True).count(),
            'total_planes_activos': Plan.query.filter_by(activo=True).count(),
            'total_solicitudes': SolicitudInstalacion.query.count(),
            'solicitudes_pendientes': SolicitudInstalacion.query.filter_by(estado='pendiente').count(),
            'solicitudes_contactadas': SolicitudInstalacion.query.filter_by(estado='contactado').count(),
            'solicitudes_agendadas': SolicitudInstalacion.query.filter_by(estado='agendado').count(),
            'coberturas_sin_planes': DashboardService._get_coberturas_sin_planes_count(),
        }
        
        return metricas
    
    @staticmethod
    def _get_coberturas_sin_planes_count():
        """
        Obtiene el conteo de coberturas activas sin planes asociados.
        
        Returns:
            int: Número de coberturas sin planes
        """
        # Obtener IDs de coberturas con planes asociados
        coberturas_con_planes = db.session.query(
            DisponibilidadPlanZona.cobertura_id
        ).distinct().all()
        coberturas_con_planes_ids = [c[0] for c in coberturas_con_planes]
        
        # Contar coberturas activas sin planes
        if coberturas_con_planes_ids:
            count = Cobertura.query.filter(
                Cobertura.activa == True,
                ~Cobertura.id.in_(coberturas_con_planes_ids)
            ).count()
        else:
            count = Cobertura.query.filter_by(activa=True).count()
        
        return count
    
    @staticmethod
    def get_solicitudes_recientes(limit=10):
        """
        Obtiene las solicitudes más recientes.
        
        Args:
            limit: Número máximo de solicitudes a retornar
            
        Returns:
            list: Lista de solicitudes recientes
        """
        solicitudes = SolicitudInstalacion.query.order_by(
            SolicitudInstalacion.fecha_creacion.desc()
        ).limit(limit).all()
        
        return solicitudes
    
    @staticmethod
    def get_resumen_por_estado():
        """
        Obtiene resumen de solicitudes agrupadas por estado.
        
        Returns:
            dict: Diccionario con conteo por estado
        """
        estados = ['pendiente', 'contactado', 'agendado', 'cancelado', 'duplicado']
        resumen = {}
        
        for estado in estados:
            count = SolicitudInstalacion.query.filter_by(estado=estado).count()
            resumen[estado] = count
        
        return resumen
    
    @staticmethod
    def get_vista_jerarquica(municipio_id=None):
        """
        Obtiene vista jerárquica del territorio.
        
        Args:
            municipio_id: Si se proporciona, filtra por municipio
            
        Returns:
            list: Lista de diccionarios con estructura jerárquica
        """
        # Obtener municipios
        query_municipios = Municipio.query.filter_by(activo=True)
        if municipio_id:
            query_municipios = query_municipios.filter(Municipio.id == municipio_id)
        
        municipios = query_municipios.order_by(Municipio.nombre).all()
        
        resultado = []
        for municipio in municipios:
            # Obtener colonias del municipio
            colonias = ColoniaComunidad.query.filter_by(
                municipio_id=municipio.id,
                activo=True
            ).order_by(ColoniaComunidad.nombre).all()
            
            colonias_info = []
            for colonia in colonias:
                # Obtener cobertura de la colonia
                cobertura = Cobertura.query.filter_by(colonia_id=colonia.id).first()
                
                cobertura_info = None
                if cobertura and cobertura.activa:
                    # Obtener planes asociados
                    planes = db.session.query(Plan).join(
                        DisponibilidadPlanZona
                    ).filter(
                        DisponibilidadPlanZona.cobertura_id == cobertura.id
                    ).order_by(Plan.orden, Plan.nombre).all()
                    
                    cobertura_info = {
                        'cobertura': cobertura,
                        'planes': planes,
                        'planes_count': len(planes)
                    }
                
                # Contar solicitudes de la colonia
                solicitudes_count = SolicitudInstalacion.query.filter_by(
                    colonia_id=colonia.id
                ).count()
                
                colonias_info.append({
                    'colonia': colonia,
                    'cobertura': cobertura_info,
                    'solicitudes_count': solicitudes_count
                })
            
            resultado.append({
                'municipio': municipio,
                'colonias': colonias_info,
                'colonias_count': len(colonias)
            })
        
        return resultado

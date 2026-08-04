"""
Servicio de Análisis de Demanda

Maneja la lógica de negocio para el análisis de demanda por zona:
- Conteo de solicitudes por municipio y colonia
- Agrupación por estado
- Identificación de zonas con alta demanda
- Diferenciación entre solicitudes con/sin cobertura
"""
from sqlalchemy import func, desc
from app.extensions import db
from app.models.solicitud import SolicitudInstalacion
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura


class AnalisisDemandaService:
    """
    Servicio para análisis de demanda por zona.
    """
    
    @staticmethod
    def get_demand_por_municipio(fecha_desde=None, fecha_hasta=None, estado=None):
        """
        Obtiene el conteo de solicitudes agrupadas por municipio.
        
        Args:
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            list: Lista de diccionarios con municipio y conteo
        """
        query = db.session.query(
            Municipio.id,
            Municipio.nombre,
            func.count(SolicitudInstalacion.id).label('total_solicitudes')
        ).join(
            SolicitudInstalacion,
            Municipio.id == SolicitudInstalacion.municipio_id
        )
        
        if fecha_desde:
            query = query.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
        
        if estado:
            query = query.filter(SolicitudInstalacion.estado == estado)
        
        query = query.group_by(Municipio.id, Municipio.nombre).order_by(desc('total_solicitudes'))
        
        resultados = query.all()
        
        return [{
            'municipio_id': r.id,
            'municipio_nombre': r.nombre,
            'total_solicitudes': r.total_solicitudes
        } for r in resultados]
    
    @staticmethod
    def get_demand_por_colonia(municipio_id=None, fecha_desde=None, fecha_hasta=None, estado=None):
        """
        Obtiene el conteo de solicitudes agrupadas por colonia.
        
        Args:
            municipio_id: Filtrar por municipio (opcional)
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            list: Lista de diccionarios con colonia, municipio y conteo
        """
        query = db.session.query(
            ColoniaComunidad.id,
            ColoniaComunidad.nombre,
            Municipio.id.label('municipio_id'),
            Municipio.nombre.label('municipio_nombre'),
            func.count(SolicitudInstalacion.id).label('total_solicitudes')
        ).join(
            SolicitudInstalacion,
            ColoniaComunidad.id == SolicitudInstalacion.colonia_id
        ).join(
            Municipio,
            ColoniaComunidad.municipio_id == Municipio.id
        )
        
        if municipio_id:
            query = query.filter(ColoniaComunidad.municipio_id == municipio_id)
        
        if fecha_desde:
            query = query.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
        
        if estado:
            query = query.filter(SolicitudInstalacion.estado == estado)
        
        query = query.group_by(
            ColoniaComunidad.id,
            ColoniaComunidad.nombre,
            Municipio.id,
            Municipio.nombre
        ).order_by(desc('total_solicitudes'))
        
        resultados = query.all()
        
        return [{
            'colonia_id': r.id,
            'colonia_nombre': r.nombre,
            'municipio_id': r.municipio_id,
            'municipio_nombre': r.municipio_nombre,
            'total_solicitudes': r.total_solicitudes
        } for r in resultados]
    
    @staticmethod
    def get_demand_con_vs_sin_cobertura(fecha_desde=None, fecha_hasta=None, estado=None):
        """
        Obtiene el conteo de solicitudes diferenciando entre zonas con y sin cobertura.
        
        Args:
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            dict: Diccionario con conteos con/sin cobertura
        """
        # Solicitudes con cobertura
        query_con = db.session.query(
            func.count(SolicitudInstalacion.id)
        ).join(
            Cobertura,
            SolicitudInstalacion.colonia_id == Cobertura.colonia_id
        ).filter(
            Cobertura.activa == True
        )
        
        # Solicitudes sin cobertura
        query_sin = db.session.query(
            func.count(SolicitudInstalacion.id)
        ).outerjoin(
            Cobertura,
            SolicitudInstalacion.colonia_id == Cobertura.colonia_id
        ).filter(
            (Cobertura.id == None) | (Cobertura.activa == False)
        )
        
        if fecha_desde:
            query_con = query_con.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
            query_sin = query_sin.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query_con = query_con.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
            query_sin = query_sin.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
        
        if estado:
            query_con = query_con.filter(SolicitudInstalacion.estado == estado)
            query_sin = query_sin.filter(SolicitudInstalacion.estado == estado)
        
        total_con = query_con.scalar() or 0
        total_sin = query_sin.scalar() or 0
        
        return {
            'con_cobertura': total_con,
            'sin_cobertura': total_sin,
            'total': total_con + total_sin
        }
    
    @staticmethod
    def get_top_colonias(limit=10, fecha_desde=None, fecha_hasta=None, estado=None):
        """
        Obtiene el top de colonias con mayor demanda.
        
        Args:
            limit: Número de resultados (default: 10)
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            estado: Filtrar por estado (opcional)
            
        Returns:
            list: Lista de top colonias con conteo
        """
        colonias = AnalisisDemandaService.get_demand_por_colonia(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            estado=estado
        )
        
        return colonias[:limit]
    
    @staticmethod
    def get_demand_por_estado(municipio_id=None, colonia_id=None, fecha_desde=None, fecha_hasta=None):
        """
        Obtiene el conteo de solicitudes agrupadas por estado.
        
        Args:
            municipio_id: Filtrar por municipio (opcional)
            colonia_id: Filtrar por colonia (opcional)
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            
        Returns:
            dict: Diccionario con conteo por estado
        """
        query = db.session.query(
            SolicitudInstalacion.estado,
            func.count(SolicitudInstalacion.id).label('total')
        )
        
        if municipio_id:
            query = query.filter(SolicitudInstalacion.municipio_id == municipio_id)
        
        if colonia_id:
            query = query.filter(SolicitudInstalacion.colonia_id == colonia_id)
        
        if fecha_desde:
            query = query.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
        
        query = query.group_by(SolicitudInstalacion.estado)
        
        resultados = query.all()
        
        return {r.estado: r.total for r in resultados}

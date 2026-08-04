"""
Servicio de Gestión de Solicitudes

Maneja la lógica de negocio para la gestión de solicitudes en el panel administrativo:
- Listar solicitudes con filtros
- Obtener detalles de solicitud
- Cambiar estado de solicitud
- Marcar solicitud como duplicada
- Exportar solicitudes a CSV
"""
import csv
import io
from datetime import datetime
from app.extensions import db
from app.models.solicitud import SolicitudInstalacion
from app.models.nota_solicitud import NotaSolicitud


class GestionSolicitudesService:
    """
    Servicio para gestión de solicitudes en panel administrativo.
    """
    
    @staticmethod
    def get_solicitudes(estado=None, fecha_desde=None, fecha_hasta=None, 
                       ordenar_por='fecha_creacion', orden='desc'):
        """
        Obtiene solicitudes con filtros opcionales.
        
        Args:
            estado: Filtrar por estado (opcional)
            fecha_desde: Filtrar desde fecha (opcional)
            fecha_hasta: Filtrar hasta fecha (opcional)
            ordenar_por: Campo para ordenar (default: fecha_creacion)
            orden: 'asc' o 'desc' (default: desc)
            
        Returns:
            list: Lista de solicitudes
        """
        query = SolicitudInstalacion.query
        
        if estado:
            query = query.filter_by(estado=estado)
        
        if fecha_desde:
            query = query.filter(SolicitudInstalacion.fecha_creacion >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(SolicitudInstalacion.fecha_creacion <= fecha_hasta)
        
        # Ordenamiento
        campo_orden = getattr(SolicitudInstalacion, ordenar_por, SolicitudInstalacion.fecha_creacion)
        if orden == 'desc':
            query = query.order_by(campo_orden.desc())
        else:
            query = query.order_by(campo_orden.asc())
        
        return query.all()
    
    @staticmethod
    def get_solicitud_by_id(solicitud_id):
        """
        Obtiene una solicitud por ID.
        
        Args:
            solicitud_id: ID de la solicitud
            
        Returns:
            SolicitudInstalacion: Solicitud si existe, None en caso contrario
        """
        return SolicitudInstalacion.query.get(solicitud_id)
    
    @staticmethod
    def cambiar_estado(solicitud_id, nuevo_estado, usuario_id=None):
        """
        Cambia el estado de una solicitud.
        
        Args:
            solicitud_id: ID de la solicitud
            nuevo_estado: Nuevo estado
            usuario_id: ID del usuario que realiza el cambio
            
        Returns:
            SolicitudInstalacion: Solicitud actualizada
            
        Raises:
            ValueError: Si la solicitud no existe o el estado es inválido
        """
        if nuevo_estado not in SolicitudInstalacion.ESTADOS_VALIDOS:
            raise ValueError(f'Estado inválido: {nuevo_estado}')
        
        solicitud = SolicitudInstalacion.query.get(solicitud_id)
        if not solicitud:
            raise ValueError(f'No existe una solicitud con ID: {solicitud_id}')
        
        solicitud.estado = nuevo_estado
        solicitud.actualizado_por = usuario_id
        
        db.session.commit()
        
        return solicitud
    
    @staticmethod
    def marcar_como_duplicada(solicitud_id, solicitud_original_id, usuario_id=None):
        """
        Marca una solicitud como duplicada de otra.
        
        Args:
            solicitud_id: ID de la solicitud a marcar como duplicada
            solicitud_original_id: ID de la solicitud original
            usuario_id: ID del usuario que realiza la acción
            
        Returns:
            SolicitudInstalacion: Solicitud actualizada
            
        Raises:
            ValueError: Si alguna solicitud no existe
        """
        solicitud = SolicitudInstalacion.query.get(solicitud_id)
        if not solicitud:
            raise ValueError(f'No existe una solicitud con ID: {solicitud_id}')
        
        solicitud_original = SolicitudInstalacion.query.get(solicitud_original_id)
        if not solicitud_original:
            raise ValueError(f'No existe una solicitud original con ID: {solicitud_original_id}')
        
        solicitud.estado = 'duplicado'
        solicitud.solicitud_duplicada_de = solicitud_original_id
        solicitud.actualizado_por = usuario_id
        
        db.session.commit()
        
        return solicitud
    
    @staticmethod
    def exportar_a_csv(solicitudes):
        """
        Exporta solicitudes a formato CSV.
        
        Args:
            solicitudes: Lista de solicitudes a exportar
            
        Returns:
            str: Contenido CSV como string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow([
            'ID', 'Fecha', 'Nombre', 'Teléfono', 'Dirección',
            'Municipio', 'Colonia', 'Plan', 'Costo Instalación',
            'Precio Mensual', 'Estado', 'Origen', 'Tipo'
        ])
        
        # Escribir datos
        for solicitud in solicitudes:
            writer.writerow([
                solicitud.id,
                solicitud.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
                solicitud.nombre_prospecto,
                solicitud.telefono_contacto,
                solicitud.direccion_especifica or '',
                solicitud.colonia.municipio.nombre if solicitud.colonia else '',
                solicitud.colonia.nombre if solicitud.colonia else '',
                solicitud.plan.nombre if solicitud.plan else '',
                float(solicitud.costo_instalacion_cotizado) if solicitud.costo_instalacion_cotizado else '',
                float(solicitud.precio_mensual_cotizado) if solicitud.precio_mensual_cotizado else '',
                solicitud.estado,
                solicitud.origen,
                solicitud.tipo
            ])
        
        return output.getvalue()
    
    @staticmethod
    def get_estadisticas():
        """
        Obtiene estadísticas básicas de solicitudes.
        
        Returns:
            dict: Diccionario con estadísticas
        """
        total = SolicitudInstalacion.query.count()
        
        por_estado = {}
        for estado in SolicitudInstalacion.ESTADOS_VALIDOS:
            por_estado[estado] = SolicitudInstalacion.query.filter_by(estado=estado).count()
        
        por_origen = {}
        for origen in SolicitudInstalacion.ORIGENES_VALIDOS:
            por_origen[origen] = SolicitudInstalacion.query.filter_by(origen=origen).count()
        
        por_tipo = {}
        for tipo in SolicitudInstalacion.TIPOS_VALIDOS:
            por_tipo[tipo] = SolicitudInstalacion.query.filter_by(tipo=tipo).count()
        
        return {
            'total': total,
            'por_estado': por_estado,
            'por_origen': por_origen,
            'por_tipo': por_tipo
        }

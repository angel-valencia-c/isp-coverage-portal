"""
Servicio de Notas de Solicitudes

Maneja la lógica de negocio para la gestión de notas en solicitudes:
- Agregar notas a solicitudes
- Listar notas de una solicitud
- Obtener detalles de nota
"""
from datetime import datetime
from app.extensions import db
from app.models.nota_solicitud import NotaSolicitud
from app.models.solicitud import SolicitudInstalacion


class NotasSolicitudesService:
    """
    Servicio para gestión de notas de solicitudes.
    """
    
    @staticmethod
    def crear_nota(solicitud_id, texto, usuario_id):
        """
        Crea una nueva nota para una solicitud.
        
        Args:
            solicitud_id: ID de la solicitud
            texto: Texto de la nota
            usuario_id: ID del usuario que crea la nota
            
        Returns:
            NotaSolicitud: Nota creada
            
        Raises:
            ValueError: Si la solicitud no existe o el texto está vacío
        """
        # Validar solicitud
        solicitud = SolicitudInstalacion.query.get(solicitud_id)
        if not solicitud:
            raise ValueError(f'No existe una solicitud con ID: {solicitud_id}')
        
        # Validar texto
        if not texto or not texto.strip():
            raise ValueError('El texto de la nota es obligatorio')
        
        # Crear nota
        nota = NotaSolicitud(
            solicitud_id=solicitud_id,
            texto=texto.strip(),
            creado_por=usuario_id
        )
        
        db.session.add(nota)
        db.session.commit()
        
        return nota
    
    @staticmethod
    def get_notas_by_solicitud(solicitud_id, orden='desc'):
        """
        Obtiene todas las notas de una solicitud.
        
        Args:
            solicitud_id: ID de la solicitud
            orden: 'asc' o 'desc' (default: desc - más recientes primero)
            
        Returns:
            list: Lista de notas
        """
        query = NotaSolicitud.query.filter_by(solicitud_id=solicitud_id)
        
        if orden == 'desc':
            query = query.order_by(NotaSolicitud.fecha_creacion.desc())
        else:
            query = query.order_by(NotaSolicitud.fecha_creacion.asc())
        
        return query.all()
    
    @staticmethod
    def get_nota_by_id(nota_id):
        """
        Obtiene una nota por ID.
        
        Args:
            nota_id: ID de la nota
            
        Returns:
            NotaSolicitud: Nota si existe, None en caso contrario
        """
        return NotaSolicitud.query.get(nota_id)
    
    @staticmethod
    def eliminar_nota(nota_id):
        """
        Elimina una nota.
        
        Args:
            nota_id: ID de la nota a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si la nota no existe
        """
        nota = NotaSolicitud.query.get(nota_id)
        if not nota:
            raise ValueError(f'No existe una nota con ID: {nota_id}')
        
        db.session.delete(nota)
        db.session.commit()
        
        return True

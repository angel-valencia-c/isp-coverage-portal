"""
Servicio de Cobertura

Maneja la lógica de negocio para la gestión de cobertura:
- Activar/desactivar cobertura por colonia
- Validaciones de negocio
- Campos de auditoría
"""
from datetime import datetime
from app.extensions import db
from app.models.cobertura import Cobertura
from app.models.colonia import ColoniaComunidad
from app.models.solicitud import SolicitudInstalacion


class CoberturaService:
    """
    Servicio para gestión de cobertura.
    """
    
    @staticmethod
    def activate(colonia_id, tipo_cobertura='total', notas=None, usuario_id=None):
        """
        Activa cobertura en una colonia.
        
        Args:
            colonia_id: ID de la colonia
            tipo_cobertura: Tipo de cobertura (total, parcial, condicional, planificada)
            notas: Notas adicionales (opcional)
            usuario_id: ID del usuario que activa la cobertura
            
        Returns:
            Cobertura: Cobertura activada
            
        Raises:
            ValueError: Si la colonia no existe, está inactiva, o ya tiene cobertura
        """
        # Validar que la colonia existe
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError(f'No existe una colonia con ID: {colonia_id}')
        
        # Validar que la colonia está activa
        if not colonia.activo:
            raise ValueError(f'La colonia "{colonia.nombre}" está inactiva')
        
        # Validar que no exista cobertura previa
        cobertura_existente = Cobertura.query.filter_by(colonia_id=colonia_id).first()
        if cobertura_existente:
            if cobertura_existente.activa:
                raise ValueError(f'La colonia "{colonia.nombre}" ya tiene cobertura activa')
            else:
                # Reactivar cobertura existente
                cobertura_existente.activa = True
                cobertura_existente.fecha_activacion = datetime.utcnow()
                cobertura_existente.fecha_desactivacion = None
                cobertura_existente.tipo_cobertura = tipo_cobertura
                if notas is not None:
                    cobertura_existente.notas = notas
                cobertura_existente.actualizado_por = usuario_id
                db.session.commit()
                return cobertura_existente
        
        # Crear nueva cobertura
        cobertura = Cobertura(
            colonia_id=colonia_id,
            activa=True,
            tipo_cobertura=tipo_cobertura,
            fecha_activacion=datetime.utcnow(),
            notas=notas,
            creado_por=usuario_id
        )
        
        db.session.add(cobertura)
        db.session.commit()
        
        return cobertura
    
    @staticmethod
    def deactivate(colonia_id, usuario_id=None, forzar=False):
        """
        Desactiva cobertura en una colonia.
        
        Args:
            colonia_id: ID de la colonia
            usuario_id: ID del usuario que desactiva la cobertura
            forzar: Si True, desactiva incluso con solicitudes pendientes
            
        Returns:
            tuple: (Cobertura desactivada, dict con info de solicitudes pendientes)
            
        Raises:
            ValueError: Si la colonia no existe o no tiene cobertura
        """
        # Validar que la colonia existe
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError(f'No existe una colonia con ID: {colonia_id}')
        
        # Obtener cobertura
        cobertura = Cobertura.query.filter_by(colonia_id=colonia_id).first()
        if not cobertura:
            raise ValueError(f'La colonia "{colonia.nombre}" no tiene cobertura')
        
        if not cobertura.activa:
            raise ValueError(f'La cobertura de "{colonia.nombre}" ya está inactiva')
        
        # Verificar solicitudes pendientes (RN-021)
        solicitudes_pendientes = SolicitudInstalacion.query.filter_by(
            colonia_id=colonia_id,
            estado='pendiente'
        ).count()
        
        info_solicitudes = {
            'tiene_pendientes': solicitudes_pendientes > 0,
            'cantidad': solicitudes_pendientes,
            'requiere_confirmacion': solicitudes_pendientes > 0 and not forzar
        }
        
        # Si hay solicitudes pendientes y no se fuerza, retornar sin desactivar
        if solicitudes_pendientes > 0 and not forzar:
            return None, info_solicitudes
        
        # Desactivar cobertura
        cobertura.activa = False
        cobertura.fecha_desactivacion = datetime.utcnow()
        cobertura.actualizado_por = usuario_id
        
        db.session.commit()
        
        return cobertura, info_solicitudes
    
    @staticmethod
    def get_by_colonia(colonia_id):
        """
        Obtiene la cobertura de una colonia.
        
        Args:
            colonia_id: ID de la colonia
            
        Returns:
            Cobertura: Cobertura si existe, None en caso contrario
        """
        return Cobertura.query.filter_by(colonia_id=colonia_id).first()
    
    @staticmethod
    def get_all(incluir_inactivas=False):
        """
        Obtiene todas las coberturas.
        
        Args:
            incluir_inactivas: Si True, incluye coberturas inactivas
            
        Returns:
            list: Lista de coberturas con información de colonia y municipio
        """
        query = Cobertura.query
        
        if not incluir_inactivas:
            query = query.filter_by(activa=True)
        
        return query.all()
    
    @staticmethod
    def update_notas(colonia_id, notas, usuario_id=None):
        """
        Actualiza las notas de una cobertura.
        
        Args:
            colonia_id: ID de la colonia
            notas: Nuevas notas
            usuario_id: ID del usuario que actualiza
            
        Returns:
            Cobertura: Cobertura actualizada
            
        Raises:
            ValueError: Si la cobertura no existe
        """
        cobertura = Cobertura.query.filter_by(colonia_id=colonia_id).first()
        if not cobertura:
            raise ValueError(f'No existe cobertura para la colonia con ID: {colonia_id}')
        
        cobertura.notas = notas
        cobertura.actualizado_por = usuario_id
        
        db.session.commit()
        
        return cobertura
    
    @staticmethod
    def update_tipo(colonia_id, tipo_cobertura, usuario_id=None):
        """
        Actualiza el tipo de cobertura.
        
        Args:
            colonia_id: ID de la colonia
            tipo_cobertura: Nuevo tipo de cobertura
            usuario_id: ID del usuario que actualiza
            
        Returns:
            Cobertura: Cobertura actualizada
            
        Raises:
            ValueError: Si la cobertura no existe o el tipo es inválido
        """
        if tipo_cobertura not in Cobertura.TIPOS_VALIDOS:
            raise ValueError(f'Tipo de cobertura inválido: {tipo_cobertura}')
        
        cobertura = Cobertura.query.filter_by(colonia_id=colonia_id).first()
        if not cobertura:
            raise ValueError(f'No existe cobertura para la colonia con ID: {colonia_id}')
        
        cobertura.tipo_cobertura = tipo_cobertura
        cobertura.actualizado_por = usuario_id
        
        db.session.commit()
        
        return cobertura
    
    @staticmethod
    def get_coberturas_con_info(incluir_inactivas=False, municipio_id=None):
        """
        Obtiene coberturas con información completa de colonia y municipio.
        
        Args:
            incluir_inactivas: Si True, incluye coberturas inactivas
            municipio_id: Si se proporciona, filtra por municipio
            
        Returns:
            list: Lista de diccionarios con información completa
        """
        query = db.session.query(Cobertura).join(ColoniaComunidad).join(
            ColoniaComunidad.municipio
        )
        
        if municipio_id:
            query = query.filter(ColoniaComunidad.municipio_id == municipio_id)
        
        if not incluir_inactivas:
            query = query.filter(Cobertura.activa == True)
        
        coberturas = query.all()
        
        resultado = []
        for cobertura in coberturas:
            colonia = cobertura.colonia
            municipio = colonia.municipio
            
            # Contar solicitudes pendientes
            solicitudes_pendientes = SolicitudInstalacion.query.filter_by(
                colonia_id=colonia.id,
                estado='pendiente'
            ).count()
            
            resultado.append({
                'cobertura': cobertura,
                'colonia': colonia,
                'municipio': municipio,
                'solicitudes_pendientes': solicitudes_pendientes
            })
        
        return resultado

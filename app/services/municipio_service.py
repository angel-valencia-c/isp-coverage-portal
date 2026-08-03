"""
Servicio de Municipios

Maneja la lógica de negocio para la gestión de municipios:
- Crear, leer, actualizar y desactivar municipios
- Validaciones de negocio
- Campos de auditoría
"""
from app.extensions import db
from app.models.municipio import Municipio


class MunicipioService:
    """
    Servicio para gestión de municipios.
    """
    
    @staticmethod
    def create(nombre, estado='Guerrero', usuario_id=None):
        """
        Crea un nuevo municipio.
        
        Args:
            nombre: Nombre del municipio
            estado: Estado al que pertenece (default: Guerrero)
            usuario_id: ID del usuario que crea el registro
            
        Returns:
            Municipio: Municipio creado
            
        Raises:
            ValueError: Si ya existe un municipio con el mismo nombre
        """
        # Validar duplicados
        existente = Municipio.query.filter_by(nombre=nombre).first()
        if existente:
            raise ValueError(f'Ya existe un municipio con el nombre: {nombre}')
        
        # Crear municipio
        municipio = Municipio(
            nombre=nombre,
            estado=estado,
            activo=True,
            creado_por=usuario_id
        )
        
        db.session.add(municipio)
        db.session.commit()
        
        return municipio
    
    @staticmethod
    def get_all(incluir_inactivos=False):
        """
        Obtiene todos los municipios.
        
        Args:
            incluir_inactivos: Si True, incluye municipios inactivos
            
        Returns:
            list: Lista de municipios
        """
        if incluir_inactivos:
            return Municipio.query.order_by(Municipio.nombre).all()
        return Municipio.query.filter_by(activo=True).order_by(Municipio.nombre).all()
    
    @staticmethod
    def get_by_id(municipio_id):
        """
        Obtiene un municipio por ID.
        
        Args:
            municipio_id: ID del municipio
            
        Returns:
            Municipio: Municipio si existe, None en caso contrario
        """
        return Municipio.query.get(municipio_id)
    
    @staticmethod
    def update(municipio_id, nombre=None, estado=None, usuario_id=None):
        """
        Actualiza un municipio existente.
        
        Args:
            municipio_id: ID del municipio a actualizar
            nombre: Nuevo nombre (opcional)
            estado: Nuevo estado (opcional)
            usuario_id: ID del usuario que actualiza el registro
            
        Returns:
            Municipio: Municipio actualizado
            
        Raises:
            ValueError: Si el municipio no existe o si el nuevo nombre ya existe
        """
        municipio = Municipio.query.get(municipio_id)
        if not municipio:
            raise ValueError(f'No existe un municipio con ID: {municipio_id}')
        
        # Validar duplicados si se cambia el nombre
        if nombre and nombre != municipio.nombre:
            existente = Municipio.query.filter_by(nombre=nombre).first()
            if existente:
                raise ValueError(f'Ya existe un municipio con el nombre: {nombre}')
        
        # Actualizar campos
        if nombre:
            municipio.nombre = nombre
        if estado:
            municipio.estado = estado
        
        municipio.actualizado_por = usuario_id
        
        db.session.commit()
        
        return municipio
    
    @staticmethod
    def deactivate(municipio_id, usuario_id=None):
        """
        Desactiva un municipio (no lo elimina).
        
        Args:
            municipio_id: ID del municipio a desactivar
            usuario_id: ID del usuario que desactiva el registro
            
        Returns:
            Municipio: Municipio desactivado
            
        Raises:
            ValueError: Si el municipio no existe
        """
        municipio = Municipio.query.get(municipio_id)
        if not municipio:
            raise ValueError(f'No existe un municipio con ID: {municipio_id}')
        
        municipio.activo = False
        municipio.actualizado_por = usuario_id
        
        db.session.commit()
        
        return municipio
    
    @staticmethod
    def activate(municipio_id, usuario_id=None):
        """
        Activa un municipio previamente desactivado.
        
        Args:
            municipio_id: ID del municipio a activar
            usuario_id: ID del usuario que activa el registro
            
        Returns:
            Municipio: Municipio activado
            
        Raises:
            ValueError: Si el municipio no existe
        """
        municipio = Municipio.query.get(municipio_id)
        if not municipio:
            raise ValueError(f'No existe un municipio con ID: {municipio_id}')
        
        municipio.activo = True
        municipio.actualizado_por = usuario_id
        
        db.session.commit()
        
        return municipio

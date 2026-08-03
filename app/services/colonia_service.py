"""
Servicio de Colonias

Maneja la lógica de negocio para la gestión de colonias/comunidades:
- Crear, leer, actualizar y desactivar colonias
- Validaciones de negocio
- Campos de auditoría
"""
from app.extensions import db
from app.models.colonia import ColoniaComunidad
from app.models.municipio import Municipio


class ColoniaService:
    """
    Servicio para gestión de colonias/comunidades.
    """
    
    @staticmethod
    def create(nombre, tipo, municipio_id, usuario_id=None):
        """
        Crea una nueva colonia/comunidad.
        
        Args:
            nombre: Nombre de la colonia/comunidad
            tipo: Tipo (colonia, comunidad, ranchería, otra)
            municipio_id: ID del municipio al que pertenece
            usuario_id: ID del usuario que crea el registro
            
        Returns:
            Colonia: Colonia creada
            
        Raises:
            ValueError: Si el municipio no existe o si ya existe una colonia con el mismo nombre en el municipio
        """
        # Validar que el municipio existe
        municipio = Municipio.query.get(municipio_id)
        if not municipio:
            raise ValueError(f'No existe un municipio con ID: {municipio_id}')
        
        if not municipio.activo:
            raise ValueError(f'El municipio "{municipio.nombre}" está inactivo')
        
        # Validar duplicados dentro del mismo municipio
        existente = ColoniaComunidad.query.filter_by(
            nombre=nombre,
            municipio_id=municipio_id
        ).first()
        if existente:
            raise ValueError(f'Ya existe una colonia con el nombre "{nombre}" en el municipio "{municipio.nombre}"')
        
        # Crear colonia
        colonia = ColoniaComunidad(
            nombre=nombre,
            tipo=tipo,
            municipio_id=municipio_id,
            activo=True,
            creado_por=usuario_id
        )
        
        db.session.add(colonia)
        db.session.commit()
        
        return colonia
    
    @staticmethod
    def get_all(incluir_inactivos=False, municipio_id=None):
        """
        Obtiene todas las colonias.
        
        Args:
            incluir_inactivos: Si True, incluye colonias inactivas
            municipio_id: Si se proporciona, filtra por municipio
            
        Returns:
            list: Lista de colonias
        """
        query = ColoniaComunidad.query
        
        if municipio_id:
            query = query.filter_by(municipio_id=municipio_id)
        
        if not incluir_inactivos:
            query = query.filter_by(activo=True)
        
        return query.order_by(ColoniaComunidad.nombre).all()
    
    @staticmethod
    def get_by_id(colonia_id):
        """
        Obtiene una colonia por ID.
        
        Args:
            colonia_id: ID de la colonia
            
        Returns:
            ColoniaComunidad: Colonia si existe, None en caso contrario
        """
        return ColoniaComunidad.query.get(colonia_id)
    
    @staticmethod
    def update(colonia_id, nombre=None, tipo=None, municipio_id=None, usuario_id=None):
        """
        Actualiza una colonia existente.
        
        Args:
            colonia_id: ID de la colonia a actualizar
            nombre: Nuevo nombre (opcional)
            tipo: Nuevo tipo (opcional)
            municipio_id: Nuevo municipio (opcional)
            usuario_id: ID del usuario que actualiza el registro
            
        Returns:
            ColoniaComunidad: Colonia actualizada
            
        Raises:
            ValueError: Si la colonia no existe, si el municipio no existe, o si el nuevo nombre ya existe
        """
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError(f'No existe una colonia con ID: {colonia_id}')
        
        # Validar duplicados si se cambia el nombre o el municipio
        if nombre or municipio_id:
            nuevo_nombre = nombre or colonia.nombre
            nuevo_municipio_id = municipio_id or colonia.municipio_id
            
            existente = ColoniaComunidad.query.filter_by(
                nombre=nuevo_nombre,
                municipio_id=nuevo_municipio_id
            ).first()
            
            if existente and existente.id != colonia_id:
                municipio = Municipio.query.get(nuevo_municipio_id)
                raise ValueError(f'Ya existe una colonia con el nombre "{nuevo_nombre}" en el municipio "{municipio.nombre}"')
        
        # Validar que el nuevo municipio existe
        if municipio_id:
            municipio = Municipio.query.get(municipio_id)
            if not municipio:
                raise ValueError(f'No existe un municipio con ID: {municipio_id}')
            if not municipio.activo:
                raise ValueError(f'El municipio "{municipio.nombre}" está inactivo')
        
        # Actualizar campos
        if nombre:
            colonia.nombre = nombre
        if tipo:
            colonia.tipo = tipo
        if municipio_id:
            colonia.municipio_id = municipio_id
        
        colonia.actualizado_por = usuario_id
        
        db.session.commit()
        
        return colonia
    
    @staticmethod
    def deactivate(colonia_id, usuario_id=None):
        """
        Desactiva una colonia (no la elimina).
        
        Args:
            colonia_id: ID de la colonia a desactivar
            usuario_id: ID del usuario que desactiva el registro
            
        Returns:
            ColoniaComunidad: Colonia desactivada
            
        Raises:
            ValueError: Si la colonia no existe
        """
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError(f'No existe una colonia con ID: {colonia_id}')
        
        colonia.activo = False
        colonia.actualizado_por = usuario_id
        
        db.session.commit()
        
        return colonia
    
    @staticmethod
    def activate(colonia_id, usuario_id=None):
        """
        Activa una colonia previamente desactivada.
        
        Args:
            colonia_id: ID de la colonia a activar
            usuario_id: ID del usuario que activa el registro
            
        Returns:
            ColoniaComunidad: Colonia activada
            
        Raises:
            ValueError: Si la colonia no existe o si el municipio está inactivo
        """
        colonia = ColoniaComunidad.query.get(colonia_id)
        if not colonia:
            raise ValueError(f'No existe una colonia con ID: {colonia_id}')
        
        # Validar que el municipio esté activo
        municipio = colonia.municipio
        if not municipio.activo:
            raise ValueError(f'No se puede activar la colonia porque el municipio "{municipio.nombre}" está inactivo')
        
        colonia.activo = True
        colonia.actualizado_por = usuario_id
        
        db.session.commit()
        
        return colonia

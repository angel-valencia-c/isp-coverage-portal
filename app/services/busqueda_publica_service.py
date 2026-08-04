"""
Servicio de Búsqueda Pública

Maneja la lógica de negocio para la búsqueda de cobertura en el portal público:
- Obtener municipios activos
- Obtener colonias por municipio
- Verificar cobertura de una colonia
- Búsqueda con autocompletado
"""
from app.extensions import db
from app.models.municipio import Municipio
from app.models.colonia import ColoniaComunidad
from app.models.cobertura import Cobertura


class BusquedaPublicaService:
    """
    Servicio para búsqueda pública de cobertura.
    """
    
    @staticmethod
    def get_municipios_activos():
        """
        Obtiene todos los municipios activos.
        
        Returns:
            list: Lista de municipios activos ordenados por nombre
        """
        return Municipio.query.filter_by(activo=True).order_by(Municipio.nombre).all()
    
    @staticmethod
    def get_colonias_por_municipio(municipio_id, solo_con_cobertura=False):
        """
        Obtiene las colonias de un municipio.
        
        Args:
            municipio_id: ID del municipio
            solo_con_cobertura: Si True, solo retorna colonias con cobertura activa
            
        Returns:
            list: Lista de colonias ordenadas por nombre
        """
        query = ColoniaComunidad.query.filter_by(
            municipio_id=municipio_id,
            activo=True
        )
        
        if solo_con_cobertura:
            # Solo colonias con cobertura activa
            query = query.join(Cobertura).filter(Cobertura.activa == True)
        
        return query.order_by(ColoniaComunidad.nombre).all()
    
    @staticmethod
    def verificar_cobertura(colonia_id):
        """
        Verifica si una colonia tiene cobertura activa.
        
        Args:
            colonia_id: ID de la colonia
            
        Returns:
            dict: Diccionario con información de cobertura
                - tiene_cobertura: bool
                - cobertura: Cobertura object or None
                - colonia: ColoniaComunidad object
        """
        colonia = ColoniaComunidad.query.get(colonia_id)
        
        if not colonia:
            return {
                'tiene_cobertura': False,
                'cobertura': None,
                'colonia': None,
                'mensaje': 'Colonia no encontrada'
            }
        
        cobertura = Cobertura.query.filter_by(
            colonia_id=colonia_id,
            activa=True
        ).first()
        
        return {
            'tiene_cobertura': cobertura is not None,
            'cobertura': cobertura,
            'colonia': colonia,
            'mensaje': 'Cobertura disponible' if cobertura else 'Sin cobertura en esta zona'
        }
    
    @staticmethod
    def buscar_colonias(termino, limite=10):
        """
        Busca colonias por nombre (autocompletado).
        
        Args:
            termino: Término de búsqueda
            limite: Número máximo de resultados
            
        Returns:
            list: Lista de colonias que coinciden con el término
        """
        if not termino or len(termino) < 2:
            return []
        
        colonias = ColoniaComunidad.query.filter(
            ColoniaComunidad.activo == True,
            ColoniaComunidad.nombre.ilike(f'%{termino}%')
        ).limit(limite).all()
        
        return colonias
    
    @staticmethod
    def buscar_municipios(termino, limite=10):
        """
        Busca municipios por nombre (autocompletado).
        
        Args:
            termino: Término de búsqueda
            limite: Número máximo de resultados
            
        Returns:
            list: Lista de municipios que coinciden con el término
        """
        if not termino or len(termino) < 2:
            return []
        
        municipios = Municipio.query.filter(
            Municipio.activo == True,
            Municipio.nombre.ilike(f'%{termino}%')
        ).limit(limite).all()
        
        return municipios

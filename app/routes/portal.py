"""
Blueprint del Portal Público

Rutas para el portal público de búsqueda de cobertura.
"""
from flask import Blueprint, render_template, request, jsonify
from app.services.busqueda_publica_service import BusquedaPublicaService

portal_bp = Blueprint('portal', __name__, url_prefix='/')


@portal_bp.route('/')
def index():
    """
    Landing page del portal público.
    """
    municipios = BusquedaPublicaService.get_municipios_activos()
    return render_template('pages/public/index.html', municipios=municipios)


@portal_bp.route('/api/municipios')
def api_municipios():
    """
    API para obtener municipios activos.
    """
    municipios = BusquedaPublicaService.get_municipios_activos()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre
    } for m in municipios])


@portal_bp.route('/api/colonias/<int:municipio_id>')
def api_colonias(municipio_id):
    """
    API para obtener colonias de un municipio.
    
    Query params:
        solo_con_cobertura: Si es 'true', solo retorna colonias con cobertura
    """
    solo_con_cobertura = request.args.get('solo_con_cobertura', 'false').lower() == 'true'
    colonias = BusquedaPublicaService.get_colonias_por_municipio(
        municipio_id,
        solo_con_cobertura=solo_con_cobertura
    )
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'tipo': c.tipo
    } for c in colonias])


@portal_bp.route('/api/verificar-cobertura/<int:colonia_id>')
def api_verificar_cobertura(colonia_id):
    """
    API para verificar cobertura de una colonia.
    """
    resultado = BusquedaPublicaService.verificar_cobertura(colonia_id)
    
    return jsonify({
        'tiene_cobertura': resultado['tiene_cobertura'],
        'mensaje': resultado['mensaje'],
        'colonia': {
            'id': resultado['colonia'].id,
            'nombre': resultado['colonia'].nombre,
            'municipio': resultado['colonia'].municipio.nombre
        } if resultado['colonia'] else None
    })


@portal_bp.route('/api/buscar-colonias')
def api_buscar_colonias():
    """
    API para buscar colonias por nombre (autocompletado).
    
    Query params:
        q: Término de búsqueda
        limite: Número máximo de resultados (default: 10)
    """
    termino = request.args.get('q', '')
    limite = request.args.get('limite', 10, type=int)
    
    colonias = BusquedaPublicaService.buscar_colonias(termino, limite)
    
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'municipio': c.municipio.nombre,
        'municipio_id': c.municipio_id
    } for c in colonias])


@portal_bp.route('/api/buscar-municipios')
def api_buscar_municipios():
    """
    API para buscar municipios por nombre (autocompletado).
    
    Query params:
        q: Término de búsqueda
        limite: Número máximo de resultados (default: 10)
    """
    termino = request.args.get('q', '')
    limite = request.args.get('limite', 10, type=int)
    
    municipios = BusquedaPublicaService.buscar_municipios(termino, limite)
    
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre
    } for m in municipios])

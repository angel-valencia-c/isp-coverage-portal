"""
Blueprint del Portal Público

Rutas para el portal público de búsqueda de cobertura.
"""
from flask import Blueprint, render_template, request, jsonify
from app.services.busqueda_publica_service import BusquedaPublicaService
from app.services.planes_publicos_service import PlanesPublicosService

portal_bp = Blueprint('portal', __name__, url_prefix='/')


@portal_bp.route('/')
def index():
    """
    Landing page del portal público.
    """
    municipios = BusquedaPublicaService.get_municipios_activos()
    return render_template('pages/public/index.html', municipios=municipios)


@portal_bp.route('/planes/<int:colonia_id>')
def planes(colonia_id):
    """
    Página de planes disponibles para una colonia con cobertura.
    """
    # Verificar cobertura
    resultado = BusquedaPublicaService.verificar_cobertura(colonia_id)
    
    if not resultado['tiene_cobertura']:
        return render_template(
            'pages/public/sin_cobertura.html',
            colonia=resultado['colonia']
        )
    
    # Obtener planes disponibles
    cobertura = resultado['cobertura']
    planes_info = PlanesPublicosService.get_planes_disponibles(cobertura.id)
    plan_destacado = PlanesPublicosService.get_plan_destacado(planes_info)
    
    return render_template(
        'pages/public/planes.html',
        colonia=resultado['colonia'],
        cobertura=cobertura,
        planes_info=planes_info,
        plan_destacado=plan_destacado
    )


@portal_bp.route('/api/planes/<int:cobertura_id>')
def api_planes(cobertura_id):
    """
    API para obtener planes disponibles en una cobertura.
    """
    planes_info = PlanesPublicosService.get_planes_disponibles(cobertura_id)
    
    return jsonify([{
        'id': p['plan'].id,
        'nombre': p['plan'].nombre,
        'velocidad_descarga': p['plan'].velocidad_descarga,
        'velocidad_subida': p['plan'].velocidad_subida,
        'precio_mensual': float(p['precio_mensual']),
        'costo_instalacion': float(p['costo_instalacion']),
        'destacado': p['plan'].destacado,
        'descripcion': p['plan'].descripcion
    } for p in planes_info])


@portal_bp.route('/api/cotizacion/<int:cobertura_id>/<int:plan_id>')
def api_cotizacion(cobertura_id, plan_id):
    """
    API para calcular cotización de un plan en una cobertura.
    """
    cotizacion = PlanesPublicosService.calcular_cotizacion(plan_id, cobertura_id)
    
    if not cotizacion:
        return jsonify({'error': 'Plan no disponible'}), 404
    
    return jsonify({
        'plan_id': cotizacion['plan'].id,
        'plan_nombre': cotizacion['plan'].nombre,
        'costo_instalacion': float(cotizacion['costo_instalacion']),
        'precio_mensual': float(cotizacion['precio_mensual']),
        'total_inicial': float(cotizacion['total_inicial']),
        'mensaje': cotizacion['mensaje']
    })


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

"""
Blueprint de Health Check

Endpoint para verificar el estado de la aplicación.
"""

from flask import Blueprint, jsonify
from app.extensions import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud
    
    Returns:
        JSON: Estado de la aplicación y conexión a BD
    """
    health_status = {
        'status': 'healthy',
        'application': 'ok',
        'database': 'unknown'
    }
    
    # Verificar conexión a base de datos
    try:
        db.session.execute(db.text('SELECT 1'))
        health_status['database'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = 'error'
        health_status['error'] = str(e)
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200

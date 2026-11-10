"""
Tests del endpoint de salud

Verifica que el endpoint /health funcione correctamente.
"""

import pytest


class TestHealthEndpoint:
    """Tests para el endpoint de health check"""
    
    def test_health_endpoint_returns_200(self, client):
        """
        Test: El endpoint /health debe retornar status 200
        """
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """
        Test: El endpoint /health debe retornar JSON
        """
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_health_endpoint_has_status_field(self, client):
        """
        Test: La respuesta debe incluir el campo 'status'
        """
        response = client.get('/health')
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_health_endpoint_has_application_field(self, client):
        """
        Test: La respuesta debe incluir el campo 'application'
        """
        response = client.get('/health')
        data = response.get_json()
        assert 'application' in data
        assert data['application'] == 'ok'
    
    def test_health_endpoint_has_database_field(self, client):
        """
        Test: La respuesta debe incluir el campo 'database'
        """
        response = client.get('/health')
        data = response.get_json()
        assert 'database' in data


class TestRootEndpoint:
    """Tests para el endpoint raíz (portal público)"""
    
    def test_root_endpoint_returns_200(self, client):
        """
        Test: El endpoint / debe retornar status 200
        """
        response = client.get('/')
        assert response.status_code == 200
    
    def test_root_endpoint_returns_html(self, client):
        """
        Test: El endpoint / debe retornar HTML (portal público)
        """
        response = client.get('/')
        assert response.content_type == 'text/html; charset=utf-8'
    
    def test_root_endpoint_has_portal_content(self, client):
        """
        Test: La respuesta debe incluir contenido del portal
        """
        response = client.get('/')
        assert b'Internet Regional' in response.data
        assert b'Verifica tu Cobertura' in response.data


class TestErrorHandling:
    """Tests para el manejo de errores"""
    
    def test_404_returns_json(self, client):
        """
        Test: Las rutas inexistentes deben retornar JSON 404
        """
        response = client.get('/nonexistent')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
    
    def test_404_has_error_field(self, client):
        """
        Test: El error 404 debe incluir el campo 'error'
        """
        response = client.get('/nonexistent')
        data = response.get_json()
        assert 'error' in data

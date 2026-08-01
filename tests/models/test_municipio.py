"""
Tests para el modelo Municipio

Verifica la creación, relaciones y campos del modelo.
"""
import pytest
from datetime import datetime
from app.models.municipio import Municipio
from app.extensions import db


class TestMunicipioModel:
    """Tests para el modelo Municipio"""
    
    def test_crear_municipio_basico(self, app, db_session):
        """Test: Se puede crear un municipio básico"""
        municipio = Municipio(
            nombre='Acapulco de Juárez',
            estado='Guerrero'
        )
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.id is not None
        assert municipio.nombre == 'Acapulco de Juárez'
        assert municipio.estado == 'Guerrero'
        assert municipio.activo is True
    
    def test_nombre_unico(self, app, db_session):
        """Test: El nombre del municipio debe ser único"""
        municipio1 = Municipio(nombre='Acapulco', estado='Guerrero')
        db_session.add(municipio1)
        db_session.commit()
        
        municipio2 = Municipio(nombre='Acapulco', estado='Guerrero')
        db_session.add(municipio2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_estado_default_guerrero(self, app, db_session):
        """Test: El estado por defecto es Guerrero"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.estado == 'Guerrero'
    
    def test_municipio_activo_por_defecto(self, app, db_session):
        """Test: Los municipios son activos por defecto"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        municipio_db = db_session.query(Municipio).filter_by(nombre='Test').first()
        assert municipio_db.activo is True
    
    def test_desactivar_municipio(self, app, db_session):
        """Test: Se puede desactivar un municipio"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        municipio.activo = False
        db_session.commit()
        
        assert municipio.activo is False
    
    def test_fecha_creacion_se_genera_automaticamente(self, app, db_session):
        """Test: fecha_creacion se genera automáticamente"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.fecha_creacion is not None
        assert isinstance(municipio.fecha_creacion, datetime)
    
    def test_fecha_modificacion_se_actualiza(self, app, db_session):
        """Test: fecha_modificacion se actualiza al modificar"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        fecha_original = municipio.fecha_modificacion
        
        municipio.nombre = 'Test Modificado'
        db_session.commit()
        
        assert municipio.fecha_modificacion is not None
        assert municipio.fecha_modificacion >= fecha_original
    
    def test_campo_creado_por_nullable(self, app, db_session):
        """Test: creado_por es nullable (para registros del portal)"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.creado_por is None
    
    def test_asignar_creado_por(self, app, db_session):
        """Test: Se puede asignar creado_por"""
        from app.models.usuario import UsuarioAdministrativo
        
        usuario = UsuarioAdministrativo(
            nombre='Admin',
            email='admin@test.com',
            password='password123',
            rol='superadministrador'
        )
        db_session.add(usuario)
        db_session.commit()
        
        municipio = Municipio(nombre='Test', creado_por=usuario.id)
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.creado_por == usuario.id
    
    def test_to_dict_incluye_campos_basicos(self, app, db_session):
        """Test: to_dict incluye todos los campos básicos"""
        municipio = Municipio(
            nombre='Acapulco',
            estado='Guerrero',
            activo=True
        )
        db_session.add(municipio)
        db_session.commit()
        
        data = municipio.to_dict()
        
        assert 'id' in data
        assert 'nombre' in data
        assert data['nombre'] == 'Acapulco'
        assert 'estado' in data
        assert data['estado'] == 'Guerrero'
        assert 'activo' in data
        assert data['activo'] is True
        assert 'fecha_creacion' in data
        assert 'fecha_modificacion' in data
    
    def test_to_dict_incluye_campos_auditoria(self, app, db_session):
        """Test: to_dict incluye campos de auditoría de BaseModel"""
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        data = municipio.to_dict()
        
        assert 'creado_por' in data
        assert 'actualizado_por' in data
    
    def test_repr(self, app, db_session):
        """Test: __repr__ muestra información útil"""
        municipio = Municipio(nombre='Acapulco', estado='Guerrero')
        
        repr_str = repr(municipio)
        assert 'Acapulco' in repr_str
        assert 'Guerrero' in repr_str
    
    def test_relacion_con_colonias(self, app, db_session):
        """Test: Un municipio puede tener muchas colonias"""
        from app.models.colonia import ColoniaComunidad
        
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        # Crear colonias asociadas
        colonia1 = ColoniaComunidad(
            nombre='Colonia 1',
            municipio_id=municipio.id
        )
        colonia2 = ColoniaComunidad(
            nombre='Colonia 2',
            municipio_id=municipio.id
        )
        db_session.add_all([colonia1, colonia2])
        db_session.commit()
        
        # Verificar relación
        assert municipio.colonias.count() == 2
        assert colonia1.municipio == municipio
        assert colonia2.municipio == municipio
    
    def test_cascade_delete_colonias(self, app, db_session):
        """Test: Al eliminar un municipio, se eliminan sus colonias"""
        from app.models.colonia import ColoniaComunidad
        
        municipio = Municipio(nombre='Test')
        db_session.add(municipio)
        db_session.commit()
        
        colonia = ColoniaComunidad(
            nombre='Colonia Test',
            municipio_id=municipio.id
        )
        db_session.add(colonia)
        db_session.commit()
        
        colonia_id = colonia.id
        
        # Eliminar municipio
        db_session.delete(municipio)
        db_session.commit()
        
        # Verificar que la colonia también se eliminó
        colonia_db = db_session.query(ColoniaComunidad).get(colonia_id)
        assert colonia_db is None

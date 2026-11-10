"""
Seeds de datos iniciales

Este script pobla la base de datos con datos de prueba mínimos para desarrollo y testing.

Datos incluidos:
- 5 municipios reales de Guerrero
- 10 colonias/comunidades reales
- 3 planes de internet genéricos
- 1 usuario administrador
- 2 coberturas de ejemplo
- 2 solicitudes de ejemplo
"""
from datetime import datetime, timezone
from app.extensions import db
from app.models import (
    UsuarioAdministrativo,
    Municipio,
    ColoniaComunidad,
    Cobertura,
    Plan,
    DisponibilidadPlanZona,
    SolicitudInstalacion,
    NotaSolicitud
)


def run_seeds():
    """
    Ejecuta los seeds de datos iniciales de forma idempotente.
    
    Esta función crea todos los datos de prueba necesarios para desarrollo.
    Es idempotente: si se ejecuta múltiples veces, no crea duplicados.
    Busca registros existentes por clave única antes de crear nuevos.
    """
    # Crear o buscar usuario administrador
    admin = UsuarioAdministrativo.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = UsuarioAdministrativo(
            nombre='Administrador Sistema',
            email='admin@example.com',
            password='admin123',
            rol='superadministrador',
            activo=True
        )
        db.session.add(admin)
        db.session.flush()
        print('  ✓ Usuario administrador creado')
    else:
        print('  → Usuario administrador ya existe')
    
    # Crear o buscar municipios reales de Guerrero
    municipios_data = [
        {'nombre': 'Acapulco de Juárez', 'estado': 'Guerrero'},
        {'nombre': 'Chilpancingo de los Bravo', 'estado': 'Guerrero'},
        {'nombre': 'Iguala de la Independencia', 'estado': 'Guerrero'},
        {'nombre': 'Taxco de Alarcón', 'estado': 'Guerrero'},
        {'nombre': 'Zihuatanejo de Azueta', 'estado': 'Guerrero'},
    ]
    
    municipios = []
    for data in municipios_data:
        municipio = Municipio.query.filter_by(nombre=data['nombre']).first()
        if not municipio:
            municipio = Municipio(
                nombre=data['nombre'],
                estado=data['estado'],
                activo=True,
                creado_por=admin.id
            )
            db.session.add(municipio)
            db.session.flush()
            print(f'  ✓ Municipio creado: {data["nombre"]}')
        else:
            print(f'  → Municipio ya existe: {data["nombre"]}')
        municipios.append(municipio)
    
    # Crear o buscar colonias/comunidades reales
    colonias_data = [
        {'nombre': 'Colonia Centro', 'tipo': 'colonia', 'municipio_idx': 0},
        {'nombre': 'Fraccionamiento Las Playas', 'tipo': 'colonia', 'municipio_idx': 0},
        {'nombre': 'Colonia Emiliano Zapata', 'tipo': 'colonia', 'municipio_idx': 1},
        {'nombre': 'Comunidad Palo Blanco', 'tipo': 'comunidad', 'municipio_idx': 1},
        {'nombre': 'Colonia Reforma', 'tipo': 'colonia', 'municipio_idx': 2},
        {'nombre': 'Ranchería El Potrero', 'tipo': 'ranchería', 'municipio_idx': 2},
        {'nombre': 'Colonia Borda', 'tipo': 'colonia', 'municipio_idx': 3},
        {'nombre': 'Comunidad El Refugio', 'tipo': 'comunidad', 'municipio_idx': 3},
        {'nombre': 'Colonia La Ropa', 'tipo': 'colonia', 'municipio_idx': 4},
        {'nombre': 'Comunidad Ixtapa', 'tipo': 'comunidad', 'municipio_idx': 4},
    ]
    
    colonias = []
    for data in colonias_data:
        colonia = ColoniaComunidad.query.filter_by(
            nombre=data['nombre'],
            municipio_id=municipios[data['municipio_idx']].id
        ).first()
        if not colonia:
            colonia = ColoniaComunidad(
                nombre=data['nombre'],
                tipo=data['tipo'],
                municipio_id=municipios[data['municipio_idx']].id,
                activo=True,
                creado_por=admin.id
            )
            db.session.add(colonia)
            db.session.flush()
            print(f'  ✓ Colonia creada: {data["nombre"]}')
        else:
            print(f'  → Colonia ya existe: {data["nombre"]}')
        colonias.append(colonia)
    
    # Crear o buscar coberturas para las primeras 2 colonias
    coberturas_data = [
        {
            'colonia_idx': 0,
            'activa': True,
            'tipo_cobertura': 'total',
            'notas': 'Cobertura total en Centro de Acapulco'
        },
        {
            'colonia_idx': 1,
            'activa': True,
            'tipo_cobertura': 'total',
            'notas': 'Cobertura total en Las Playas'
        }
    ]
    
    coberturas = []
    for data in coberturas_data:
        cobertura = Cobertura.query.filter_by(colonia_id=colonias[data['colonia_idx']].id).first()
        if not cobertura:
            cobertura = Cobertura(
                colonia_id=colonias[data['colonia_idx']].id,
                activa=data['activa'],
                tipo_cobertura=data['tipo_cobertura'],
                fecha_activacion=datetime.now(timezone.utc),
                notas=data['notas'],
                creado_por=admin.id
            )
            db.session.add(cobertura)
            db.session.flush()
            print(f'  ✓ Cobertura creada para: {colonias[data["colonia_idx"]].nombre}')
        else:
            print(f'  → Cobertura ya existe para: {colonias[data["colonia_idx"]].nombre}')
        coberturas.append(cobertura)
    
    # Crear o buscar planes de internet
    planes_data = [
        {
            'nombre': 'Básico 20Mbps',
            'velocidad_descarga': 20,
            'velocidad_subida': 5,
            'precio_mensual': 299.00,
            'descripcion': 'Plan básico para navegación y redes sociales',
            'orden': 1,
            'destacado': False
        },
        {
            'nombre': 'Estándar 50Mbps',
            'velocidad_descarga': 50,
            'velocidad_subida': 10,
            'precio_mensual': 499.00,
            'descripcion': 'Plan estándar para streaming y trabajo remoto',
            'orden': 2,
            'destacado': True
        },
        {
            'nombre': 'Premium 100Mbps',
            'velocidad_descarga': 100,
            'velocidad_subida': 20,
            'precio_mensual': 799.00,
            'descripcion': 'Plan premium para gaming y múltiples dispositivos',
            'orden': 3,
            'destacado': False
        },
    ]
    
    planes = []
    for data in planes_data:
        plan = Plan.query.filter_by(nombre=data['nombre']).first()
        if not plan:
            plan = Plan(
                nombre=data['nombre'],
                velocidad_descarga=data['velocidad_descarga'],
                velocidad_subida=data['velocidad_subida'],
                precio_mensual=data['precio_mensual'],
                descripcion=data['descripcion'],
                activo=True,
                orden=data['orden'],
                destacado=data['destacado'],
                creado_por=admin.id
            )
            db.session.add(plan)
            db.session.flush()
            print(f'  ✓ Plan creado: {data["nombre"]}')
        else:
            print(f'  → Plan ya existe: {data["nombre"]}')
        planes.append(plan)
    
    # Crear o buscar disponibilidad de planes en coberturas
    for cobertura in coberturas:
        for plan in planes:
            disponibilidad = DisponibilidadPlanZona.query.filter_by(
                cobertura_id=cobertura.id,
                plan_id=plan.id
            ).first()
            if not disponibilidad:
                disponibilidad = DisponibilidadPlanZona(
                    cobertura_id=cobertura.id,
                    plan_id=plan.id,
                    costo_instalacion=500.00,
                    disponible=True,
                    creado_por=admin.id
                )
                db.session.add(disponibilidad)
                db.session.flush()
                print(f'  ✓ Disponibilidad creada: {plan.nombre} en {cobertura.colonia.nombre}')
            else:
                print(f'  → Disponibilidad ya existe: {plan.nombre} en {cobertura.colonia.nombre}')
    
    # Crear o buscar solicitudes de ejemplo
    solicitudes_data = [
        {
            'nombre_prospecto': 'Juan Pérez García',
            'telefono_contacto': '7441234567',
            'direccion_especifica': 'Calle Hidalgo #123, entre Av. Costera y Calle 5',
            'municipio_idx': 0,
            'colonia_idx': 0,
            'plan_idx': 1,
            'costo_instalacion_cotizado': 500.00,
            'precio_mensual_cotizado': 499.00,
            'estado': 'pendiente',
            'origen': 'portal',
            'tipo': 'solicitud_cobertura'
        },
        {
            'nombre_prospecto': 'María López Hernández',
            'telefono_contacto': '7449876543',
            'direccion_especifica': 'Blvd. Renacimiento #456, Fracc. Las Playas',
            'municipio_idx': 0,
            'colonia_idx': 1,
            'plan_idx': 2,
            'costo_instalacion_cotizado': 500.00,
            'precio_mensual_cotizado': 799.00,
            'estado': 'contactado',
            'origen': 'portal',
            'tipo': 'solicitud_cobertura'
        }
    ]
    
    solicitudes = []
    for data in solicitudes_data:
        solicitud = SolicitudInstalacion.query.filter_by(
            telefono_contacto=data['telefono_contacto']
        ).first()
        if not solicitud:
            solicitud = SolicitudInstalacion(
                nombre_prospecto=data['nombre_prospecto'],
                telefono_contacto=data['telefono_contacto'],
                direccion_especifica=data['direccion_especifica'],
                municipio_id=municipios[data['municipio_idx']].id,
                colonia_id=colonias[data['colonia_idx']].id,
                plan_id=planes[data['plan_idx']].id,
                costo_instalacion_cotizado=data['costo_instalacion_cotizado'],
                precio_mensual_cotizado=data['precio_mensual_cotizado'],
                estado=data['estado'],
                origen=data['origen'],
                tipo=data['tipo'],
                creado_por=None  # Creada por el portal público
            )
            db.session.add(solicitud)
            db.session.flush()
            print(f'  ✓ Solicitud creada: {data["nombre_prospecto"]}')
        else:
            print(f'  → Solicitud ya existe: {data["nombre_prospecto"]}')
        solicitudes.append(solicitud)
    
    # Crear o buscar notas en las solicitudes
    notas_data = [
        {
            'solicitud_idx': 0,
            'texto': 'Prospecto interesado en plan Estándar. Llamar mañana.'
        },
        {
            'solicitud_idx': 1,
            'texto': 'Contactado exitosamente. Agendó instalación para el viernes.'
        }
    ]
    
    for data in notas_data:
        nota = NotaSolicitud.query.filter_by(
            solicitud_id=solicitudes[data['solicitud_idx']].id,
            texto=data['texto']
        ).first()
        if not nota:
            nota = NotaSolicitud(
                solicitud_id=solicitudes[data['solicitud_idx']].id,
                texto=data['texto'],
                creado_por=admin.id
            )
            db.session.add(nota)
            db.session.flush()
            print(f'  ✓ Nota creada para solicitud de: {solicitudes[data["solicitud_idx"]].nombre_prospecto}')
        else:
            print(f'  → Nota ya existe para solicitud de: {solicitudes[data["solicitud_idx"]].nombre_prospecto}')
    
    # Commit final
    db.session.commit()
    
    print('\n✓ Seeds completados exitosamente (modo idempotente)')


if __name__ == '__main__':
    """
    Permite ejecutar el script directamente con: python seeds/initial_data.py
    """
    from app import create_app
    
    app = create_app('development')
    with app.app_context():
        run_seeds()

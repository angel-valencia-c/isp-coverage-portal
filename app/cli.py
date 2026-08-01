"""
Comandos CLI personalizados para Flask

Este módulo registra comandos CLI adicionales para la aplicación Flask.
"""
import click
from flask import current_app
from flask.cli import with_appcontext


def register_commands(app):
    """
    Registra comandos CLI personalizados en la aplicación Flask.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.cli.command('seed')
    @with_appcontext
    def seed_command():
        """
        Ejecutar seeds de datos iniciales.
        
        Este comando pobla la base de datos con datos de prueba mínimos
        para desarrollo y testing.
        """
        from seeds.initial_data import run_seeds
        
        click.echo('Ejecutando seeds de datos iniciales...')
        try:
            run_seeds()
            click.echo(click.style('✓ Seeds completados exitosamente', fg='green'))
        except Exception as e:
            click.echo(click.style(f'✗ Error al ejecutar seeds: {str(e)}', fg='red'))
            raise
    
    @app.cli.command('seed-reset')
    @with_appcontext
    def seed_reset_command():
        """
        Resetear base de datos y ejecutar seeds.
        
        Este comando elimina todas las tablas, las recrea y ejecuta los seeds.
        Útil para desarrollo.
        """
        from app.extensions import db
        from seeds.initial_data import run_seeds
        
        click.echo('Reseteando base de datos...')
        try:
            db.drop_all()
            db.create_all()
            click.echo('✓ Base de datos reseteada')
            
            click.echo('Ejecutando seeds...')
            run_seeds()
            click.echo(click.style('✓ Seeds completados exitosamente', fg='green'))
        except Exception as e:
            click.echo(click.style(f'✗ Error: {str(e)}', fg='red'))
            raise

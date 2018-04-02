"""WSGI application declaration."""
import app

application = app.create(settings_module_name='settings.prod')

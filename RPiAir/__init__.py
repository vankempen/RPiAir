from flask import Flask

# Flask application
app = Flask('__name__', template_folder='RPiAir/templates', static_folder='RPiAir/static')
app.config.from_object('config')

from RPiAir import views


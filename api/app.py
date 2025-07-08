# -*- coding: utf-8 -*-
"""The app module, containing the app factory function.
"""
from flask import Flask

def create_app(config_object="settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__.split(".")[0])

    return app

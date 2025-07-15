# -*- coding: utf-8 -*-
"""The app module, containing the app factory function.
"""
from flask import Flask

class MyJSONEncoder():
    pass

def create_app(config_object="settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    app.json = MyJSONEncoder(app)

    return app

# -*- coding: utf-8 -*-
"""The app module, containing the app factory function.
"""
import decimal
import datetime
import logging
import sys
import os

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_babel.speaklater import LazyString
from flask import make_response
from flask import jsonify
from flask import Blueprint

from logging.handlers import RotatingFileHandler
from inspect import getmembers

import api.view.entry


HERE = os.path.abspath(os.path.dirname(__file__))

class MyJSONEncoder(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, (decimal.Decimal, datetime.date, datetime.time, LazyString)):
            return str(o)
        
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        
        return o


def configure_logger(app: Flask):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s")

    if app.debug:
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    log_file = app.config['LOG_PATH']
    if log_file and log_file != "/dev/stdout":
        file_handler = RotatingFileHandler(log_file, maxBytes=2 ** 30, backupCount=7)
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))


def register_error_handlers(app: Flask):
    """Register error handlers."""

    def render_error(error):
        import traceback
        app.logger.error(traceback.format_exc())
        error_code = getattr(error, "code", 500)
        if not str(error_code).isdigit():
            error_code = 400
        return make_response(jsonify(message=str(error)), error_code)

    for errcode in app.config.get("ERROR_CODES") or [400, 401, 403, 404, 405, 500, 502]: 
        app.errorhandler(errcode)(render_error)

    app.handle_exception = render_error


def configure_upload_dir(app: Flask):
    upload_dir = app.config.get("UPLOAD_DIRECTORY", "uploaded_files")
    common_setting_path = os.path.join(HERE, upload_dir)
    print(f"获取的值：${common_setting_path}")
    for path in [common_setting_path]:
        if not os.path.exists(path):
            app.logger.warning(f"{path}, not exist, ready to create it...")
            os.makedirs(path)

    # aaa = app.config["UPLOAD_DIRECTORY_FULL"]
    aaa = app.config.get("UPLOAD_DIRECTORY_FULL", "default_path")
    print(aaa)
    app.config["UPLOAD_DIRECTORY_FULL"] = common_setting_path
    aaa = app.config["UPLOAD_DIRECTORY_FULL"]
    print(f"最终的值: ${aaa}")
   

def register_blueprints(app: Flask):
    for item in getmembers(api.view.entry):
        if item[0].startswith("blueprint") and isinstance(item[1], Blueprint):
            app.register_blueprint(item[1])


def create_app(config_object="settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    app.json = MyJSONEncoder(app)

    configure_logger(app)
    register_error_handlers(app)
    configure_upload_dir(app)

    register_blueprints(app)

    return app


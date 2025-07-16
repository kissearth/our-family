import os

from flask import Blueprint

from flask_restful import Api

from .test import TestView

HERE = os.path.abspath(os.path.dirname(__file__))

# test
blueprint_test = Blueprint("test_api", __name__, url_prefix="/api/test")
test_rest = Api(blueprint_test)
test_rest.add_resource(TestView, TestView.url_prefix)

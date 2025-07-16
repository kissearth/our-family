# -*- coding:utf-8 -*-

import os
import sys
import six

from flask import jsonify
from flask import send_file
from flask_restful import Resource

from inspect import getmembers, isclass


class APIView(Resource):
    method_decorators = []

    def __init__(self):
        super(APIView, self).__init__()

    @staticmethod
    def jsonify(*args, **kwargs):
        return jsonify(*args, **kwargs)
    
    @staticmethod
    def send_file(*args, **kwargs):
        return send_file(*args, **kwargs)


API_PACKAGE = os.path.abspath(os.path.dirname(__file__))


def register_resources(resource_path, resource_api):
    pass




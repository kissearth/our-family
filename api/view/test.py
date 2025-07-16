# -*- coding:utf-8 -*-

import datetime

from api.resource import APIView

class TestView(APIView):
    url_prefix = "/test"

    def get(self):
        return self.jsonify(msg="这是get方法")

    def post(self):
        return self.jsonify(msg="这是post方法")

    def delete(self):
        return self.jsonify(msg="这是delete方法")
    
    def put(self):
        return self.jsonify(msg="这是put方法")
    
    
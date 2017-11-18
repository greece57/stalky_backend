import threading
from flask import request, jsonify
from flask_restful import Resource

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph


class UserApi(Resource):

    def get(self):
        response = jsonify({"OK":"works"})
        response.status_code = 200
        return response

    def post(self):
        json_data = request.get_json(force=True)
        
        id = json_data["id"]
        access_token = json_data["access_token"]
        
        add_user_thread = FuncThread(lambda: FbGraph.addUser(id, access_token))
        add_user_thread.start()
        
        response = jsonify({"OK":"Adding User"})
        response.status_code = 200
        return response
    

            

        

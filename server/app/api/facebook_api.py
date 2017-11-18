import threading
from flask import request, jsonify
from flask_restful import Resource

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph


class FacebookAPI(Resource):

    def get(self, id=None):
        if id is None:
            response = jsonify({"Error":"Please specify an id"})
            response.status_code = 400
            return response
        
        add_user_thread = FuncThread(lambda: FbGraph.addUser(id))
        add_user_thread.start()
        
        response = jsonify({"OK":"Adding User"})
        response.status_code = 200
        return response
    

            

        

import threading
from flask import request, jsonify
from flask_restful import Resource
from app.model import Image

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph
from app.external_apis.cognitive_face import FaceApi
from app.model.user import User

class UserApi(Resource):

    def get(self):
        id = request.args.get("id")
        if id == None:
            response = jsonify({"Error":"Specify a user id"})
            response.status_code = 400
            return response

        if not User.select().where(User.fb_id == id).exists():
            response = jsonify({"Error":"No user with specified id '" + str(id) + "'"})

        status = FaceApi().get_training_status(id)
        response = jsonify(status)
        response.status_code = 200
        return response


    def post(self):
        json_data = request.get_json(force=True)
        
        id = json_data["id"]
        print(id)
        access_token = request.headers.get('authorization')
        
        add_user_thread = FuncThread(lambda: FbGraph(access_token).addUser(id))
        add_user_thread.start()
        
        response = jsonify({"OK":"Adding User"})
        response.status_code = 200
        return response

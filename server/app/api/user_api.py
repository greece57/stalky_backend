import threading
from flask import request, jsonify
from flask_restful import Resource
from app.model import Image

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph

import cognitive_face as CF

class UserApi(Resource):

    def get(self):
        image = Image.get()
        url = image.source_url
        face_exist = []
        KEY = 'e6caf64b32b24455a6a4e2e91a386f76'  
        CF.Key.set(KEY)
        BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  
        CF.BaseUrl.set(BASE_URL)

        result = CF.face.detect(url)

        for face in result:
            rect = face["faceRectangle"]
            exists = UserApi.contains(image.x, image.y, rect["left"], rect["top"],rect["width"], rect["height"])
            face_exist.append(exists)

        response = jsonify(face_exist)
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

    def contains(fb_x, fb_y, rect_x, rect_y, rect_width, rect_height):
        return (rect_x <= fb_x <= rect_x + rect_width and
            rect_y <= fb_y <= rect_y + rect_height)

    

            

        

from flask import request, jsonify
from flask_restful import Resource
from app.model import Image

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph
from app.external_apis.cognitive_face import FaceApi
from app.model.user import User

class IdentifyApi(Resource):

    def get(self):
        from flask import send_from_directory
        from app import APP

        filename = request.args.get("filename")
        if filename == None:
            response = jsonify({"Error":"Didn't specify a filename"})
            response.status_code = 400
            return response

        return send_from_directory(APP.config['UPLOAD_FOLDER'], filename)

    def post(self):
        import os
        from werkzeug.utils import secure_filename
        from app import APP

        id = request.args.get("id")
        if id == None:
            response = jsonify({"Error":"Specify a picture id"})
            response.status_code = 400
            return response

        if 'file' not in request.files:
            response = jsonify({"Error":"No file part"})
            response.status_code = 400
            return response

        file = request.files['file']
        filename = file.filename
        
        if filename == '':
            response = jsonify({"Error":"No file name"})
            response.status_code = 400
            return response

        file_suffix = filename.rsplit('.', 1)[1].lower()
        if file and file_suffix == "jpg":
            filename = secure_filename(file.filename)
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
        else:
            response = jsonify({"Error" : "Wrong file extension: '" + str(file_suffix) + "'"})
            response.status_code = 400
            return response

        #image_url = "http://" + str(APP.config['WHOAMI']) + "/api/identify?filename=" + str(filename)
        #friend, confidence = FaceApi().identify_face(id, image_url)
        #response = jsonify({"Friend Name":friend.name,
        #                "Confidence":confidence})
        response = jsonify({"Friend Name":"friend.name",
                        "Confidence":"confidence"})
        response.status_code = 200
        return response


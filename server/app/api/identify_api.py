import os
from flask import request, jsonify
from flask_restful import Resource
from app.model import Image

from app.helper.func_thread import FuncThread
from app.external_apis.fb_graph import FbGraph
from app.external_apis.cognitive_face import FaceApi
from app.model.user import User

class IdentifyApi(Resource):

    def get(self):
        from flask import send_file
        from werkzeug.utils import secure_filename
        from app import APP

        filename = request.args.get("filename")
        if filename == None:
            response = jsonify({"Error":"Didn't specify a filename"})
            response.status_code = 400
            return response

        path = os.path.join("..", APP.config['UPLOAD_FOLDER'], filename)
        print(path)
        if secure_filename(filename):
            return send_file(path)
        else:
            return jsonify({"Fuck":"you"})

    def post(self):
        from werkzeug.utils import secure_filename
        from app import APP

        id = request.args.get("id")
        if id == None:
            response = jsonify({"Error":"Specify a picture id"})
            response.status_code = 400
            return response

        if 'file' not in request.files:
            response = jsonify(request.files)
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
            print(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
        else:
            response = jsonify({"Error" : "Wrong file extension: '" + str(file_suffix) + "'"})
            response.status_code = 400
            return response

        image_url = "http://" + str(APP.config['WHOAMI']) + "/api/identify?filename=" + str(filename)
        print(image_url)
        friend, confidence = FaceApi().identify_face(id, image_url)
        if friend == 0:
            response = jsonify({"Message":"Idiot not found"})
            response.status_code = 204
            return response

        response = jsonify({"Friend Name":str(friend.name),
                        "Confidence":str(confidence)})
        response.status_code = 200
        return response


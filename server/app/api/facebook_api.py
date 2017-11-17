import facebook as fb
from flask import request, jsonify
from flask_restful import Resource

FB_API_TOKEN = "EAACEdEose0cBANR43pM6zG8YekjRpPsVFOdT7tdR9ij7LDF9w4RJ3x6Uk3xkRgb2RogUbA4kqiLb4BFKkpuD3z9oHgmc2HdKeVHGaqTDMYy8sIPMkvtIpYqX4xfmiO5G8QH90kxxoR1Xrgu9UosZAEmL0giHjiUp68h4S7U78QZAVZCqRV3hYc4cDAkj5x39ZAMTn7c9YgZDZD"
fb_graph = fb.GraphAPI(access_token=FB_API_TOKEN)

class FacebookAPI(Resource):

    def get(self, id=None):
        if id is None:
            response = jsonify({"Error":"Please specify an id"})
            response.status_code = 400
            return response
        
        id = id + "/friends"
        info = fb_graph.get_object(id=id, fields="name,photos")

        output = []

        for user in info["data"]:
            if "photos" in user:
                for photo in user["photos"]["data"]:
                    photo_id = photo["id"]
                    image, x, y = FacebookAPI.tags(user["name"],photo_id)
                    output.append(user["name"] + " " + image + "; x: " + str(x) + "; y: " + str(y))

        response = jsonify(output)
        response.status_code = 200
        return response
    
    def tags(name, photo_id):
        tagged_photos = fb_graph.get_object(id=photo_id, fields="images,tags")
        image = tagged_photos["images"][0]["source"]

        for tags in tagged_photos["tags"]["data"]:
            if tags["name"] == name:
                return image,tags["x"], tags["y"]
            
        return image, 0, 0

            

        

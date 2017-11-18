import facebook as fb
from app.model import *

class FbGraph():

    def __init__(self, fb_access_token):
        self.fb_graph = fb.GraphAPI(access_token=fb_access_token)

    def addUser(self, id):
        from app.external_apis.cognitive_face import FaceApi

        id = str(id)
        u = User.create(fb_id=id, person_group=id)
        u.save()
        id = id + "/friends"
        info = self.fb_graph.get_object(id=id, fields="name,photos")

        for friend in info["data"]:
            if "photos" in friend:
                f = Friend.create(fb_id=friend["id"], name=friend["name"], person_id="", user=u)
                f.save()
                for photo in friend["photos"]["data"]:
                    photo_id = photo["id"]
                    source, x, y = self.tags(f.name,photo_id)
                    i = Image(image_fb_id=photo_id, source_url=source, x=x, y=y, persisted_face_id="", friend=f)
                    i.save()


        FaceApi().train_faces_for_user(u)

    def get_user_info(self, user_id):
        info = self.fb_graph.get_object(id=user_id, fields="about,birthday,education,work")
        return info

    def tags(self, name, photo_id):
        tagged_photos = self.fb_graph.get_object(id=photo_id, fields="images,tags")
        image = tagged_photos["images"][0]["source"]
        width = tagged_photos["images"][0]["width"]
        height = tagged_photos["images"][0]["height"]
        

        for tags in tagged_photos["tags"]["data"]:
            if tags["name"] == name:
                x = width * (tags["x"]/100)
                y = height * (tags["y"]/100)
                return image,x,y
            
        return image, 0, 0
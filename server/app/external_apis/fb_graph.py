import facebook as fb
from app.model import *

FB_API_TOKEN = "EAACEdEose0cBALCctoYzbmHOcaUZAUWkklvt9mZAKoGlwQAFZCBjbDT2kWXsDy7JfqAvZCvCIOFnRx12L3YsHJdmkZA3UYuAskFiR0f2RACtUWMwcdZAdhCIWSBteXHaavjex9TopTEgalzz9O3vL6yGYbkGsRpTw4ovQASYw8DM9dt724LPrGlThYZCHAv6xILneuZAjtIHUwZDZD"
fb_graph = fb.GraphAPI(access_token=FB_API_TOKEN)

class FbGraph():

    def addUser(id, access_token):
        u = User.create(fb_id=id, access_token=access_token, person_group=id)
        u.save()
        id = id + "/friends"
        info = fb_graph.get_object(id=id, fields="name,photos")

        output = []

        for friend in info["data"]:
            if "photos" in friend:
                f = Friend.create(fb_id=friend["id"], name=friend["name"], face_id="", user=u)
                f.save()
                for photo in friend["photos"]["data"]:
                    photo_id = photo["id"]
                    source, x, y = FbGraph.tags(f.name,photo_id)
                    i = Image(image_fb_id=photo_id, source_url=source, x=x, y=y, friend=f)
                    i.save()

    def tags(name, photo_id):
        tagged_photos = fb_graph.get_object(id=photo_id, fields="images,tags")
        image = tagged_photos["images"][0]["source"]
        width = tagged_photos["images"][0]["width"]
        height = tagged_photos["images"][0]["height"]
        

        for tags in tagged_photos["tags"]["data"]:
            if tags["name"] == name:
                x = width * (tags["x"]/100)
                y = height * (tags["y"]/100)
                return image,x,y
            
        return image, 0, 0
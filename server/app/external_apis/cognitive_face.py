import cognitive_face as CF
from app.model import *

class FaceApi():

    def __init__(self):
        KEY = 'e6caf64b32b24455a6a4e2e91a386f76'  
        CF.Key.set(KEY)
        BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  
        CF.BaseUrl.set(BASE_URL)

    def get_training_status(self, id):
        return CF.person_group.get_status(id)

    def train_faces_for_user(self, user):
        person_group_id = user.fb_id
        CF.person_group.delete(person_group_id)
        CF.person_group.create(person_group_id)
        for friend in Friend.select().where(Friend.user==user):
            new_person = CF.person.create(person_group_id, friend.name)
            friend.person_id = new_person["personId"]
            friend.save()
            for image in Image.select().where(Image.friend==friend):
                rect = self.get_rectangle_in_image(image)
                if rect != 0:
                    rect_param = str(rect["left"]) + "," + str(rect["top"]) + "," + str(rect["width"]) + "," + str(rect["height"])
                    new_face = CF.person.add_face(image.source_url, person_group_id, friend.person_id, target_face=rect_param)
                    image.persisted_face_id = new_face["persistedFaceId"]
                    image.save()

        CF.person_group.train(person_group_id)

    def identify_face(self, id, image_url):
        print("alive 1")
        faces = CF.face.detect(image_url)
        if len(faces) == 1:
            print("alive 2")
            identify_response = CF.face.identify([faces[0]["faceId"]], id)
            print(identify_response)
            canidate = identify_response[0]["candidates"][0]
            print("alive 4")
            if Friend.select().where(Friend.person_id == canidate["personId"]).exists():
                return Friend().get(Friend.person_id == canidate["personId"]), canidate["confidence"]
            else:
                return 0, 0
        return 0,0


    def get_rectangle_in_image(self, image):
        result = CF.face.detect(image.source_url)
        for face in result:
            rect = face["faceRectangle"]
            if self.contains(image.x, image.y, rect["left"], rect["top"],rect["width"], rect["height"]):
                return rect
        return 0

    def contains(self, fb_x, fb_y, rect_x, rect_y, rect_width, rect_height):
        return (rect_x <= fb_x <= rect_x + rect_width and
                rect_y <= fb_y <= rect_y + rect_height)


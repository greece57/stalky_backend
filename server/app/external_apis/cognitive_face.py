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
        person_groups = CF.person_group.lists()
        for p_group in person_groups:
            if p_group["personGroupId"] == person_group_id:
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

    def identify_face(self, id, image_url, x, y, width, height):
        print("alive 1")
        faces = CF.face.detect(image_url)
        print(len(faces))
        if len(faces) == 1:
            print("alive 2")
            identify_response = CF.face.identify([faces[0]["faceId"]], id)
            print(identify_response)
            if len(identify_response[0]["candidates"]):
                canidate = identify_response[0]["candidates"][0]
            else:
                return 1,0
            print(canidate)
            print("alive 4")
            if Friend.select().where(Friend.person_id == canidate["personId"]).exists():
                return Friend().get(Friend.person_id == canidate["personId"]), canidate["confidence"]
            else:
                return 0, 0
        elif len(faces) > 1:
            for face in faces:
                rect = face["faceRectangle"]
                if(self.overlap(x,x+width,y, y+height,rect["left"],rect["left"]+width,rect["top"],rect["top"]+height)):
                    print("alive5")
                    identify_response = CF.face.identify([face["faceId"]], id)
                    if len(identify_response[0]["candidates"]):
                        canidate = identify_response[0]["candidates"][0]
                    else:
                        return 1,0
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

    def overlap(self, recta_left, recta_right, recta_top, recta_bottom, rectb_left, rectb_right, rectb_top, rectb_bottom):
        print("r_l: " + str(recta_left) + "r_r: " + str(recta_right) +"r_t: " + str(recta_top) +"r_b: " + str(recta_bottom))
        print("r2_l: " + str(rectb_left) + "r2_r: " + str(rectb_right) +"r2_t: " + str(rectb_top) +"r2_b: " + str(rectb_bottom))
        return (recta_left < rectb_right and recta_right > rectb_left and recta_top > rectb_bottom and recta_bottom < rectb_top ) 
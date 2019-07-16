from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.picture import PictureModel
from PIL import Image
import base64
from io import BytesIO

buffered = BytesIO()

def merge_image(base, icon):
    x_off = 0
    y_off = 0
    if icon == 0:
        png = "trumpr.png"
        x_off = 30
    elif icon == 1:
        png = "boldr.png"
        x_off = 200
    elif icon == 2:
        png = "42r.png"
        x_off = 200
        y_off = 200
    img = Image.open(BytesIO(base64.b64decode(base))).convert("RGBA")
    p = Image.open(png).convert("RGBA")
    x, y = p.size
    img.paste(p, (x_off, y_off, x + x_off, y+ y_off), p)
    #img.save("test.png", format="png")
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


class Picture(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
                        type=str,
                        required=True,
                        help="image is necessary")
    parser.add_argument('like',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('date',
                        type=str,
                        required=False,
                        help="")    
    parser.add_argument('comments',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('username',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('icon',
                        type=int,
                        required=False,
                        help="")

    def post(self):
        data = Picture.parser.parse_args()        
        picture = PictureModel(**data)
        picture.image = merge_image(data.image, data.icon)
        #print(merge_image(data.image, data.icon))

        try:
            picture.save_to_db()            
        except:            
            return {"message": "An error occured inserting the picture."}, 500
        return {"message": "Success"}        


    def put(self, id):
        data = Picture.parser.parse_args()
        picture = PictureModel.find_by_id(id)
        
        if picture is None:
            picture = PictureModel(**data)

        else:
            picture.image = data['image']
            picture.date = data['date']
            picture.like = data['like']
            picture.comments = data['comments']
            picture.username = data['username']            

        picture.save_to_db()
        return picture.json()

    def delete(self, id):
        picture = PictureModel.find_by_id(id)
        if picture:
            picture.delete_from_db()
        return({'mesage': 'Picture deleted'})

    def get(self, id):
        picture = PictureModel.find_by_id(id)
        if picture:
            return picture.json()
        return {'message': 'Picture not found'}, 404


class PictureList(Resource):
    def get(self):
        return {'pictures': [x.json() for x in PictureModel.query.all()]}
        # return {'pictures': list(map(lambda x: x.json(), PictureModel.query.all()))}
        # return {'pictures': [picture.json() for picture in PictureModel.query.all()]}class PictureList(Resource):

    def delete(self):
        PictureModel.delete_all()
        return({'mesage': 'All Picturelist deleted'})


class PictureEdit(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('like',
                        type=int,
                        required=False,
                        help="")
    parser.add_argument('date',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('image',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('comments',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('username',
                        type=str,
                        required=False,
                        help="")

    def put(self, id):
        data = PictureEdit.parser.parse_args()
        picture = PictureModel.find_by_id(id)

        picture.image = data['image']
        picture.date = data['date']
        picture.like = data['like']
        picture.image = data['image']
        picture.comments = data['comments']
        picture.username = data['username']

        picture.save_to_db()
        return picture.json()

    def get(self, id):

        picture = PictureModel.find_by_id(id)
        if picture:
            return picture.json()
        return {'message': 'Picture not found'}, 404

    def post(self, id):
        if PictureModel.find_by_id(id):
            return {'message': "An picture with id `{}` already exists".format(id)}, 400

        data = Picture.parser.parse_args()

        picture = PictureModel(id, **data)

        try:
            picture.save_to_db()

        except:
            # Internal Server Error
            return {"message": "An error occured inserting the picture."}, 500
        return {"message": "Success"}
        # return picture.json(), 201

    def delete(self, id):
        picture = PictureModel.find_by_id(id)
        if picture:
            picture.delete_from_db()
        return({'mesage': 'Picture deleted'})

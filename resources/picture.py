from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.picture import PictureModel


class Picture(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('like',
                        type=int,
                        required=False,
                        help="")
    parser.add_argument('date',
                        type=lambda d: datetime.strptime(d, '%m%d%h').date(),
                        required=False,
                        help="")
    """ parser.add_argument('imgpath',
                        type=str,
                        required=True,
                        help="path is necessary") """
    parser.add_argument('comments',
                        type=str,
                        required=False,
                        help="")
    parser.add_argument('username',
                        type=str,
                        required=False,
                        help="")

    def post(self, imgpath):
        if PictureModel.find_by_imgpath(imgpath):
            return {'message': "An picture with imgpath `{}` already exists".format(imgpath)}, 400

        data = Picture.parser.parse_args()
        # print(data)
        picture = PictureModel(imgpath, **data)

        try:
            picture.save_to_db()

        except:
            # Internal Server Error
            return {"message": "An error occured inserting the picture."}, 500
        return {"message": "Success"}
        # return picture.json(), 201

    def put(self, imgpath):
        data = Picture.parser.parse_args()
        picture = PictureModel.find_by_imgpath(imgpath)
        print(data)
        if picture is None:
            picture = PictureModel(imgpath, **data)

        else:
            picture.imgpath = data['imgpath']
            picture.date = data['date']
            picture.like = data['like']
            picture.comments = data['comments']
            picture.username = data['username']

        picture.save_to_db()
        return picture.json()

    def delete(self, imgpath):
        picture = PictureModel.find_by_imgpath(imgpath)
        if picture:
            picture.delete_from_db()
        return({'mesage': 'Picture deleted'})

    def get(self, imgpath):
        picture = PictureModel.find_by_imgpath(imgpath)
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
    parser.add_argument('imgpath',
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

        picture.imgpath = data['imgpath']
        picture.date = data['date']
        picture.like = data['like']
        picture.imgpath = data['imgpath']
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

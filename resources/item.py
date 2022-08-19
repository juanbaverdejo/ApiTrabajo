from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot by left blank"
                        )

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'messege': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()

        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

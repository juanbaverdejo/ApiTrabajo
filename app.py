from flask import Flask
from flask_restful import Api
from db import db
from resources.item import Item

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://juanbaverde:armada2055@localhost:5432/audit_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/item/<string:name>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)
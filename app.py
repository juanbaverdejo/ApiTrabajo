from flask import Flask, render_template, request, redirect
from flask_restful import Api
from db import db
from models.item import ItemModel
from resources.item import Item


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://juanbaverde:armada2055@localhost:5432/audit_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    items = None
    if request.method == 'POST' and 'name' in request.form:
        try:
            itemNuevo = ItemModel(name=request.form.get("name"),
                                  price=request.form.get("price")
                                  )
            ItemModel.save_to_db(itemNuevo)
        except Exception as e:
            print("Failed to add item")
            print(e)
    items = ItemModel.query.all()
    return render_template('home.html', items=items)
@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        item = ItemModel.query.filter_by(name=oldname).first()
        item.name = newname
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    name= request.form.get("name")
    item = ItemModel.query.filter_by(name=name).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/")

api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
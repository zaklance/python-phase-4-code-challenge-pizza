#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_all_rest():
    if request.method == 'GET':
        rest = Restaurant.query.all()
        return [r.to_dict(rules=['-restaurant_pizzas']) for r in rest], 200

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_one_rest(id):
    rest = Restaurant.query.filter(Restaurant.id == id).first()

    if not rest:
        return {'error': 'Restaurant not found'}, 404
    
    if request.method == 'GET':
        return rest.to_dict(), 200
    elif request.method == 'DELETE':
        db.session.delete(rest)
        db.session.commit()
        return {}, 204
    
@app.route('/pizzas', methods=['GET'])
def get_all_pies():
    if request.method == 'GET':
        pizza_pies = Pizza.query.all()
        return [p.to_dict(rules=['-restaurant_pizzas']) for p in pizza_pies], 200

@app.route('/restaurant_pizzas', methods=['POST'])
def get_all_rest_pizza():
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_rest_pizzas = RestaurantPizza(
                price=data.get('price'),
                pizza_id=data.get('pizza_id'),
                restaurant_id=data.get('restaurant_id')
            )
        except ValueError as e:
            return {'errors': ['validation errors']}, 400
        db.session.add(new_rest_pizzas)
        db.session.commit()

        return new_rest_pizzas.to_dict(), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)

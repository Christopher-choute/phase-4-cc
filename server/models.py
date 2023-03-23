from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    pizzas = association_proxy('restaurant_pizzas', 'pizza')
    serialize_rules = ('-restaurant_pizzas', '-pizzas.restaurants')

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship("RestaurantPizza", backref = "restaurant")

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    restaurants = association_proxy('restaurant_pizzas', 'restaurant')
    serialize_rules = ('-restaurant_pizzas', '-restaurants.pizzas')

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    restaurant_pizzas = db.relationship("RestaurantPizza", backref = "pizza")
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    #just gonna go ahead and add everything I can here... just incase 
    serialize_rules = ('-restaurant.pizzas', '-pizza.restaurants', '-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    @validates('price')
    def validates_strength(self,key, price):
        if price >= 1 or price <= 30:
            return price
        raise ValueError({"error": "Invalid price bozo!!!"})




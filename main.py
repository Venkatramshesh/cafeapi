from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
from distutils.util import strtobool

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cafech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


cafe_apikey = "O0XLPI1AQ0UCKtvkc-StFw"

##Cafe TABLE Configuration
class cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    web_url = db.Column(db.String(500), nullable=False)
    #img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    #db.create_all()
    return render_template("index.html")


@app.route("/random",methods =['GET', 'POST'])
def getrandomcafe():
    random_cafe = random.choice(cafe.query.all())
    return jsonify(cafe={
        # Omit the id from the response
        # "id": random_cafe.id,
        "name": random_cafe.name,
        "web_url": random_cafe.web_url,
        #"img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "amenities": {
            "seats": random_cafe.seats,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "has_sockets": random_cafe.has_sockets,
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
        }
    })

@app.route("/all", methods=['GET', 'POST'])
def allcafe():
    random_cafe = cafe.query.all()
    n = 0
    allcafe = {}
    for cafes in random_cafe:
        allcafe[n]={
            # Omit the id from the response
            # "id": random_cafe.id,
            "name": cafes.name,
            "web_url": cafes.web_url,
            #"img_url": cafes.img_url,
            "location": cafes.location,
            "amenities": {
                "seats": cafes.seats,
                "has_toilet": cafes.has_toilet,
                "has_wifi": cafes.has_wifi,
                "has_sockets": cafes.has_sockets,
                "can_take_calls": cafes.can_take_calls,
                "coffee_price": cafes.coffee_price,
            }
        }
        n+=1
    return (jsonify(allcafe))

@app.route("/search", methods=['GET', 'POST'])
def searchcafe():
    cafenamel = request.args.get('location')
    my_cafe = cafe.query.filter_by(location=cafenamel).first()
    if my_cafe==None:
        return jsonify(error={"Not Found": "Sorrry, we don't have a cafe at that location"})
    else:
        return jsonify(cafe={
        # Omit the id from the response
        # "id": random_cafe.id,
        "name": my_cafe.name,
        #"map_url": my_cafe.map_url,
        "web_url": my_cafe.web_url,
        "location": my_cafe.location,
        "amenities": {
            "seats": my_cafe.seats,
            "has_toilet": my_cafe.has_toilet,
            "has_wifi": my_cafe.has_wifi,
            "has_sockets": my_cafe.has_sockets,
            "can_take_calls": my_cafe.can_take_calls,
            "coffee_price": my_cafe.coffee_price,
        }
    })

## HTTP POST - Create Record
@app.route("/add",methods=['GET', 'POST'])
def add():
    #db.create_all()
   post = cafe(name=request.form['name'],web_url=request.form['web_url'],location=request.form['location'],seats=request.form['seats'],has_toilet=strtobool(request.form['has_toilet']),
                has_wifi=strtobool(request.form['has_wifi']), has_sockets=strtobool(request.form['has_sockets']), can_take_calls=strtobool(request.form['can_take_calls']),coffee_price=request.form['coffee_price'])
   db.session.add(post)
   db.session.commit()
   return jsonify(reponse={"success": "Successfully added the new cafe"})

@app.route("/update-price/<cafe_id>")
def update(cafe_id):
    cafe_to_update = cafe.query.filter_by(id=cafe_id).first()
    if cafe_to_update==None:
        return jsonify(reponse={"error": "Sorry a cafe with that id was not found in database."}), 404
    else:
        cafe_to_update.coffee_price=request.args.get('new_price')
        db.session.commit()
        return jsonify(reponse={"success": "Successfully updated the price"}),200

# ## HTTP DELETE - Delete Record
@app.route("/reportclosed/<cafe_id>",methods=['DELETE'])
def reportclosed(cafe_id):
    api_key = request.args.get('api_key')
    if api_key != cafe_apikey:
        return jsonify(reponse={"error": "Sorry that's not allowed. Make sure you have the correct api_key."})
    else:
        cafe_to_update = db.session.query(cafe).get(cafe_id)
        #cafe_to_update = cafe.query.filter_by(id=cafe_id).first()
        if cafe_to_update==None:
            return jsonify(reponse={"error": {"Not Found" : "Sorry a cafe with that id was not found in database."}})
        else:
            cafe.query.filter_by(id=cafe_id).delete()
            db.session.commit()
            return jsonify(reponse={"success": "Successfully deleted the shop"})

if __name__ == '__main__':
    app.run(debug=True)

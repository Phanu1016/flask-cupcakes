"""Flask app for Cupcakes"""
from flask import Flask, flash, request, redirect, render_template, session, jsonify
from models import connect_database, database, Cupcake

app = Flask(__name__)
app.app_context().push()

DATABASE_NAME = 'cupcakes'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "Phanu!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_database(app)

def serialize(cupcake):
    """ Serialize cupcake object to JSON """
    return {"id":cupcake.id, "flavor":cupcake.flavor, "size":cupcake.size, "rating":cupcake.rating, "image":cupcake.image}


@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/api/cupcakes')
def return_all_cupcakes():
    """ Get data about all cupcakes """
    return jsonify(cupcakes=[serialize(cupcake) for cupcake in Cupcake.query.all()])

@app.route('/api/cupcakes/<int:cupcake_id>')
def return_singular_cupcake(cupcake_id):
    """ Get data about a single cupcake """
    return jsonify(cupcake=serialize(Cupcake.query.get_or_404(cupcake_id)))

@app.route('/api/cupcakes', methods=['POST'])
def add_new_cupcake():
    """ Create a cupcake with flavor, size, rating and image data from the body of the request. """
    new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json.get('image', "https://tinyurl.com/demo-cupcake"))
    database.session.add(new_cupcake)
    database.session.commit()
    return (jsonify(cupcake=serialize(new_cupcake)),201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """ Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    database.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)
    database.session.commit()
    return jsonify(cupcake=serialize(cupcake))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Delete cupcake with the id passed in the URL """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    database.session.delete(cupcake)
    database.session.commit()
    return {"message": "Deleted"}


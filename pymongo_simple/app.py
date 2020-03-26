from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)

@app.route("/", methods=["GET"])
def index():
    return "Hello World!"


@app.route('/stars', methods=['GET'])
def get_all_stars():
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/star/<name>', methods=['GET'])
def get_one_star(name):
    star = mongo.db.stars
    stars = star.find({'name': name})
    output = []
    for s in stars:
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/add_star', methods=['GET'])
def add_star():
    star = mongo.db.stars
    name = request.args.get('name')
    distance = request.args.get('distance')
    star_id = star.insert_one({'name': name, 'distance': float(distance)})
    return jsonify({'result': "star {} successfully added".format(name)})


if __name__ == '__main__':
    app.run(debug=True)

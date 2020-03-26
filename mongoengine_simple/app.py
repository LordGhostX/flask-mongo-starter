from flask import Flask, request, Response
from database.db import initialize_db
from database.models import Movie
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)


@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)


@app.route('/add', methods=['GET'])
def add_movie():
    body = request.args
    movie = Movie(**body).save()
    id = movie.id
    return {'id': str(id)}, 200


@app.route('/update/<id>', methods=['GET'])
def update_movie(id):
    body = request.args
    Movie.objects.get(id=id).update(**body)
    return '', 200


@app.route('/delete/<id>', methods=['GET'])
def delete_movie(id):
    movie = Movie.objects.get(id=id).delete()
    return '', 200


@app.route('/movies/<id>')
def get_movie(id):
    movies = Movie.objects.get(id=id).to_json()
    return Response(movies, mimetype="application/json", status=200)


if __name__ == '__main__':
    app.run(debug=True)

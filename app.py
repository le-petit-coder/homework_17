# app.py

from models import *
from flask_restx import Api, Resource

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):

        director_id = request.args.get('director_id')
        query = Movie.query
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        genre_id = request.args.get('genre_id')
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        return MovieSchema(many=True).dump(query.all()), 200

    def post(self):
        data = request.json
        try:
            db.session.add(Movie(**data))
            db.session.commit()
            return "Posted"
        except Exception as e:
            db.session.rollback()
            return "Failed not posted"


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        return MovieSchema().dump(Movie.query.get(mid)), 200

    def put(self, mid):
        data = request.json
        try:
            result = Movie.query.filter(Movie.id == mid).one()
            result.title = data.get('title')
            db.session.add(result)
            db.session.commit()
            return "Updated", 200
        except Exception as e:
            db.session.rollback()
            return "Failed not updated"

    def delete(self, mid):
        try:
            result = Movie.query.filter(Movie.id == mid).one()
            db.session.delete(result)
            db.session.commit()
            return "Deleted"
        except Exception as e:
            db.session.rollback()
            return "Failed not deleted"


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return DirectorSchema(many=True).dump(Director.query.all()), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        return DirectorSchema().dump(Director.query.get(did)), 200


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        return GenreSchema(many=True).dump(Genre.query.all()), 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        return GenreSchema().dump(Genre.query.get(gid)), 200


if __name__ == '__main__':
    app.run(debug=True)

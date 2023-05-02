from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\tmp\\movie.db'
db = SQLAlchemy(app)
app.app_context().push()  # <-- Add this line


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(80))
    runtime = db.Column(db.Integer)

    def to_dict(self):
        movie_dict = {
            "title": self.title,
            "release_year": self.release_year,
            "director": self.director,
            "runtime": self.runtime,
        }
        return movie_dict

    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/movies')
def movies():
    movies_list = Movie.query.all()
    return render_template("movies.html", movies=movies_list)


@app.route('/movies/<int:id>')
def movie(id):
    movie = Movie.query.get(id)
    return render_template("movie.html", movie=movie)


@app.route("/movies/delete/<int:id>", methods=["GET", "POST"])
def movies_delete(id):
    movie = Movie.query.get(id)
    if request.method == "POST":
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for("movies"))
    return render_template("movies_delete.html", movie=movie)


@app.route("/movies/modify/<int:id>", methods=["GET", "POST"])
def movies_modify(id):
    movie = Movie.query.get(id)
    if request.method == "POST":
        movie.title = request.form.get("title")
        movie.release_year = request.form.get("release_year")
        movie.director = request.form.get("director")
        movie.runtime = request.form.get("runtime")
        db.session.commit()
        return redirect(url_for("movies"))
    return render_template("movies_modify.html", movie=movie)


@app.route("/movies/create", methods=["GET", "POST"])
def movies_create():
    if request.method == "POST":
        title = request.form.get("title")
        release_year = request.form.get("release_year")
        director = request.form.get("director")
        runtime = request.form.get("runtime")
        new_movie = Movie(title=title, release_year=release_year,
                          director=director, runtime=runtime)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("movies"))
    return render_template("movies_create.html")


@app.route("/api/test")
def api_test():
    data = {"text": "hello"}
    return jsonify(data)


def movie_to_dict(movie_obj):
    movie_dict = {
        "title": movie_obj.title,
        "release_year": movie_obj.release_year,
        "director": movie_obj.director,
        "runtime": movie_obj.runtime,
    }
    return movie_dict


@app.route("/api/time")
def api_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = {"current_time": current_time}
    return jsonify(data)


@app.route("/api/movies/read")
def read():
    id = request.args.get("id")
    if id:
        movie = Movie.query.get(id)
        return jsonify(movie.to_dict())

    title = request.args.get("title")
    release_year = request.args.get("release_year")
    director = request.args.get("director")
    runtime = request.args.get("runtime")

    if title or release_year or director or runtime:
        movies = []
        if title:
            movies += Movie.query.filter_by(title=title)
        if release_year:
            movies += Movie.query.filter_by(release_year=release_year)
        if director:
            movies += Movie.query.filter_by(director=director)
        if runtime:
            movies += Movie.query.filter_by(runtime=runtime)
        
        movies_list = []
        for movie in movies:
            movies_list.append(movie.to_dict())
        return jsonify(movies_list)

    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_list.append(movie.to_dict())
    return jsonify(movie_list)


@app.route("/api/movies/delete")
def api_movies_delete():
    id = request.args.get("id")
    if id:
        movie = Movie.query.get(id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return jsonify(movie.to_dict())
        else:
            return jsonify({"message": "not found"})
    else:
        return jsonify({"message": "no ID given"})

@app.route("/api/movies/create", methods = ["POST"])
def api_movies_create():
    title = request.form.get("title")
    release_year = request.form.get("release_year")
    director = request.form.get("director")
    runtime = request.form.get("runtime")
    if title and release_year and director and runtime:
        new_movie = Movie(
            title=title,
            release_year=release_year,
            director=director,
            runtime=runtime
        ) 
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict())
    return jsonify({"message": "data missing"})


@app.route("/api/movies/update", methods = ["POST"])
def api_movies_update():
    id = request.args.get("id")
    if id:
        movie = Movie.query.get(id)
        if movie:
            movie.title = request.form.get("title", movie.title)
            movie.release_year = request.form.get("release_year", movie.release_year)
            movie.director = request.form.get("director", movie.director)
            movie.runtime = request.form.get("runtime", movie.runtime)
            db.session.commit()
            return jsonify(movie.to_dict())
        return jsonify({"message": "not found"})
    return jsonify({"message": "no ID sent"})



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\tmp\\movie.db'
db = SQLAlchemy(app)
app.app_context().push() # <-- Add this line

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(80))
    runtime = db.Column(db.Integer)
    
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

@app.route("/movies/delete/<int:id>", methods = ["GET", "POST"])
def movies_delete(id):
    movie = Movie.query.get(id)
    if request.method == "POST":
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for("movies"))
    return render_template("movies_delete.html", movie=movie)

@app.route("/movies/modify/<int:id>", methods = ["GET", "POST"])
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


@app.route("/movies/create", methods = ["GET", "POST"])
def movies_create():
    if request.method == "POST":
        title = request.form.get("title")
        release_year = request.form.get("release_year")
        director = request.form.get("director")
        runtime = request.form.get("runtime")
        new_movie = Movie(title=title, release_year=release_year, director=director, runtime=runtime)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("movies"))
    return render_template("movies_create.html")

@app.route("/api/test")
def api_test():
    data = {"text": "hello"}
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)
    







import requests
import json

data = {"title": "Yüzüklerin Efendisi, iki kule",
        "release_year": 2002,
        "director": "Peter Jackson",
        "runtime": 121
        }

url = "http://localhost:5000/api/movies/create"
response = requests.post(url, data=data)

movie = response.json()

for x, y in movie.items():
    print('"', x, '"', ":", '"', y, '"', sep="")

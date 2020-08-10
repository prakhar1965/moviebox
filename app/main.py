from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
import re
import joblib

df = joblib.load('dataframe.pkl')
model = joblib.load('model.pkl')
col = ['index', 'title_year', 'imdb_score', 'duration', 'movie_title', 'genres']
df = df.filter(col, axis=1)
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/api/get-movies/")
def get_all_movies():
    return jsonify({})


@app.route("/api/get-movies/<prefix>")
def get_movies(prefix):
    list_movies = search_movies(prefix)
    try:
        data = pd.concat([df[df['movie_title'] == x] for x in list_movies])
        x = data.to_json(orient='records')
        return x
    except:
        return jsonify({})


@app.route("/api/get-recommendation", methods=['GET', 'POST'])
def get_recommendation():
    try:
        liked_movies = request.get_json(force=True)
        movies = liked_movies['watched_movies']
        list_of_movies = []
        for i in movies:
            list_of_movies.append((int(i), movies[i]['rating']))
        score_movies = []
        for ele in list_of_movies:
            if len(score_movies) == 0:
                score_movies = model[ele[0]] * (ele[1] - 2)
            else:
                score_movies = list(np.add(np.array(score_movies), np.array(model[ele[0]]) * (ele[1] - 2)))
        similar_movies = list(enumerate(score_movies))
        high = 50 + len(list_of_movies)
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[0:high]
        unique_movies = seen(sorted_similar_movies, list_of_movies)
        data = pd.concat([df[df['index'] == x] for x in unique_movies])
        x = data.to_json(orient='records')
        return x
    except:
        return jsonify({})

def search_movies(s):
    list_of_movies = [pics for pics in df.movie_title if re.search(s.lower(), pics.lower())]
    return sorted(list_of_movies, key=lambda x: x.lower().find(s.lower()))[0:7]

def get_index(title):
    return df[df['movie_title'] == title].index.values[0]


def get_title(index):
    return df[df['index'] == index].movie_title.values[0]

def seen(sorted_movies, list_movies):
    s_movie = [x[0] for x in sorted_movies]
    l_movie = [x[0] for x in list_movies]
    final_list = []
    for x in s_movie:
        if x not in l_movie:
            final_list.append(x)
    return final_list


if __name__ == '__main__':
    app.run()
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

features = ['genres', 'movie_title', 'plot_keywords', 'director_name']
used_cols = ['title_year', 'imdb_score', 'duration', 'movie_imdb_link']
used_cols.extend(features)

def func(row):
    return row['genres'].replace('|', ' ') + " " + row['movie_title'] + " " + row['plot_keywords'].replace('|', ' ') + " " + row['director_name']

def func1(row):
    return row['genres'].replace('|', ' ')


def get_index(title):
    return df[df['movie_title'] == title].index.values[0]


def get_title(index):
    return df[df['index'] == index].movie_title.values[0]


if __name__ == '__main__':
    df = pd.read_csv('movie_metadata.csv', usecols=used_cols)
    for feature in features:
        df[feature] = df[feature].fillna('')
    df['title_year'] = df['title_year'].fillna(2010)
    df['duration'] = df['duration'].fillna(100)
    df['movie_title'] = df.apply(lambda row: str(row['movie_title']).strip(), axis=1)
    df.drop_duplicates(subset=['movie_title'], keep='first', inplace=True)
    df.reset_index(inplace=True)

    df['index'] = range(len(df))
    df['genres'] = df.apply(func1, axis=1)
    joblib.dump(df, 'dataframe.pkl')
    print("Dataframe Model dumped!")
    df['features'] = df.apply(func, axis=1)
    vector = CountVectorizer()
    model = vector.fit_transform(df['features'])
    cosine_mat = cosine_similarity(model)
    joblib.dump(cosine_mat, 'model.pkl')
    print("Similarity Model dumped!")

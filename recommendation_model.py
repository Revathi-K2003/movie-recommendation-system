import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import requests

OMDB_API_KEY = '5a6f4c81'

# Load CSV globally (to use in fetch_movie_details)
movies_df = pd.read_csv('movies.csv')


def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        poster = data.get('Poster')
        if poster and poster != "N/A":
            return poster
        else:
            return '/static/default.jpg'
    except:
        return '/static/default.jpg'


def fetch_youtube_trailer(title):
    """Returns a YouTube search link for the trailer of the given movie title."""
    search_query = f"{title} trailer"
    return f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"


def get_recommendations(title):
    conn = sqlite3.connect('movies.db')
    movies = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()

    if title not in movies['original_title'].values:
        return []

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['overview'].fillna(""))

    title_to_index = {t: i for i, t in enumerate(movies['original_title'])}
    idx = title_to_index[title]

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    for i, score in sim_scores:
        movie = movies.iloc[i]
        homepage = movie['homepage'] if 'homepage' in movie and pd.notna(movie['homepage']) else ''
        poster = fetch_poster(movie['original_title'])

        recommended_movies.append({
            'title': movie['original_title'],
            'overview': movie['overview'],
            'poster': poster,
            'homepage': homepage
        })

    return recommended_movies


def fetch_movie_details(title):
    movie = movies_df[movies_df['original_title'].str.lower() == title.lower()]
    
    if movie.empty:
        return None

    movie = movie.iloc[0]

    return {
        'title': movie['original_title'],
        'plot': movie.get('overview', ''),
        'genre': movie.get('genres', ''),
        'production_companies': movie.get('production_companies', ''),
        'vote_count': movie.get('vote_count', ''),
        'vote_average': movie.get('vote_average', ''),
        'release_date': movie.get('release_date', ''),
        'spoken_language': movie.get('original_language', ''),
        'tagline': movie.get('tagline', ''),
        'homepage': movie.get('homepage', ''),
        'poster': fetch_poster(movie['original_title']),
        'trailer_url': fetch_youtube_trailer(movie['original_title'])  # use new function
    }

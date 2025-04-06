from flask import Flask, render_template, request
import sqlite3
from recommendation_model import get_recommendations, fetch_movie_details, fetch_poster, fetch_youtube_trailer

app = Flask(__name__)

@app.route('/movie/<title>')
def movie_detail(title):
    movie_data = fetch_movie_details(title)
    if not movie_data:
        return "Movie not found", 404

    # Add poster and trailer info
    movie_data['poster'] = fetch_poster(title)
    movie_data['trailer_url'] = fetch_youtube_trailer(title)

    return render_template('movie_details.html', movie=movie_data)


def get_all_titles():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_title FROM movies')
    titles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return titles

@app.route('/', methods=['GET', 'POST'])
def home():
    all_titles = get_all_titles()
    recommendations = []
    selected_title = None

    if request.method == 'POST':
        selected_title = request.form.get('movie_title')
        if selected_title:
            recommendations = get_recommendations(selected_title)

    return render_template(
        'index.html',
        all_titles=all_titles,
        recommendations=recommendations,
        selected_title=selected_title
    )

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))

# movie-recommendation-system -- link --https://movie-recommendation-system-2-77wl.onrender.com
A web-based movie recommender system built with Flask that suggests similar movies based on content-based filtering using TF-IDF and cosine similarity.

--Features
Recommend similar movies based on selected input
TF-IDF vectorization of movie metadata (genres, overview)
Cosine similarity-based ranking
Flask-powered backend with dynamic routing
Responsive frontend using HTML and CSS
Lightweight SQLite database for movie data

--Tech Stack
Layer	Technology
Backend	Python, Flask
Frontend	HTML, CSS
ML/NLP	TF-IDF, Cosine Similarity (sklearn)
Database	SQLite

--How It Works
User selects a movie from the dropdown.
The backend retrieves metadata and calculates TF-IDF vectors.
Cosine similarity scores are computed with all other movies.
The top N most similar movies are returned and displayed.

--ML Technique Used
Content-Based Filtering: Based on movie metadata (genres, overview).
TF-IDF Vectorization: Converts text data into numerical vectors.
Cosine Similarity: Measures similarity between movie vectors.

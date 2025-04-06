"""
import pandas as pd
import sqlite3

# Load data
df = pd.read_csv('movies.csv')
df = df.dropna(subset=['original_title', 'overview'])
df = df[['original_title', 'overview']]

# Save to SQLite DB
conn = sqlite3.connect('movies.db')
df.to_sql('movies', conn, if_exists='replace', index=False)
conn.close()
print("✅ movies.db created successfully")
"""
import pandas as pd
import sqlite3

# Load the CSV
df = pd.read_csv('movies.csv')

# Drop rows where title or overview is missing
df = df.dropna(subset=['original_title', 'overview'])

# Fill empty optional fields with empty strings
df['genres'] = df.get('genres', '')
df['homepage'] = df.get('homepage', '')

# Select only the needed columns
df = df[['original_title', 'overview', 'genres', 'homepage']]

# Save to SQLite DB
conn = sqlite3.connect('movies.db')
df.to_sql('movies', conn, if_exists='replace', index=False)
conn.close()

print("✅ movies.db created successfully with poster, genre, and homepage.")

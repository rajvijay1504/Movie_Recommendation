#########################################################################################################
# Notes:
# 1. Fixed "Sky High" bug.
# 2. Supports multi-word movie search.
# 3. Resolves duplicate movie names (e.g., Sky High 2005 vs Sky High 2003).
#########################################################################################################

import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import sys
import os

pd.set_option('display.max_columns', None)

def load_content_data():
    # Load dataset.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return pd.read_csv(os.path.join(dir_path, 'static/combined_metadata_table.csv'))

def find_movie(keyword, df):
    # Filter movies by keyword.
    return df[df['title'].str.contains(keyword, flags=re.IGNORECASE, regex=True)]

def pick_movie(df):
    # List movies for selection.
    print('\nFound movies:\n')
    for i in range(len(df)):
        row = df.iloc[i]
        print(i, ':', row['title'], f"({row['year']})")
    idx = int(input('\nSelect movie id: '))
    valid = (0 <= idx < len(df))
    return valid, idx

def filter_by_genre(title, df):
    # Filter by genre.
    genres = df[df['title'] == title]['genre'].iloc[0].split(', ')
    mask = df['genre'].str.contains(genres[0], na=False)
    for g in genres[1:]:
        mask |= df['genre'].str.contains(g, na=False)
    return df[mask]

def filter_by_year(title, df, window=30):
    # Filter by year range.
    year = df[df['title'] == title]['year'].iloc[0]
    return df[(df['year'] >= year - window) & (df['year'] <= year + window)]

def filter_by_language(title, df):
    # Filter by language.
    langs = df[df['title'] == title]['language'].iloc[0].split(', ')
    mask = df['language'].str.contains(langs[0], na=False)
    for lang in langs[1:]:
        mask |= df['language'].str.contains(lang, na=False)
    return df[mask]

def remove_spaces(source):
    # Remove spaces in name fields.
    cols = ['director', 'writer', 'production_company', 'actors']
    src = source.copy()
    for col in cols:
        src[col] = src[col].str.replace(' ', '', regex=True)
        src[col] = src[col].str.replace(',', ' ', regex=True)
    return src

def compute_tfidf(source):
    # Compute TF-IDF from selected columns.
    cols = ['country', 'director', 'writer', 'production_company', 'actors',
            'description', 'overview', 'tagline']
    texts, titles, imdbids = [], [], []
    for i in range(source.shape[0]):
        row = source.iloc[i]
        text = ' '.join(str(row[col]) for col in cols)
        texts.append(text)
        titles.append(row['title'])
        imdbids.append(row['imdb_title_id'])
    df_text = pd.DataFrame({'IMDBid': imdbids, 'Title': titles, 'Content': texts})
    vect = TfidfVectorizer()
    X = vect.fit_transform(df_text['Content'])
    return X, df_text

def cosine_sim(X, df_text, title):
    # Compute cosine similarity.
    idx = df_text[df_text['Title'] == title].index[0]
    d1 = X[idx].toarray()[0]
    mag1 = np.linalg.norm(d1)
    sims = []
    for i in range(X.shape[0]):
        row = X[i].toarray()[0]
        sims.append(np.dot(d1, row) / (mag1 * np.linalg.norm(row)))
    sim_series = pd.Series(sims).sort_values(ascending=False)
    sim_series = sim_series.iloc[1:6]  # Exclude the movie itself.
    return pd.DataFrame(sim_series)

def get_recommendations(df_text, sim_df):
    # Merge similarity scores with data.
    res = pd.merge(sim_df, df_text, left_index=True, right_index=True)
    return res.rename({0: 'Score'}, axis='columns')

def print_results(res, num=6):
    # Print top recommendations.
    print('Top recommendations:\n')
    for i in range(1, num):
        row = res.iloc[i]
        print('IMDB ID:', row['IMDBid'], '| Title:', row['Title'])
    print('\nBye!\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception(f'Enter 1 movie title; given {len(sys.argv)-1}')
    keyword = ' '.join(sys.argv[1:])
    df_all = load_content_data()
    df_pick = find_movie(keyword, df_all)
    if df_pick.empty:
        raise Exception('\nNo movie found.\n')
    valid, idx = pick_movie(df_pick)
    if not valid:
        raise Exception('Invalid selection.')
    title = df_pick.iloc[idx]['title']
    src = filter_by_genre(title, df_all)
    src = filter_by_year(title, src)
    src = filter_by_language(title, src)
    src = remove_spaces(src)
    X, df_text = compute_tfidf(src)
    sim_df = cosine_sim(X, df_text, title)
    res = get_recommendations(df_text, sim_df)
    print_results(res)

import pandas as pd
from html_template_functions import compute_tfidf, cosine_sim, get_recommendations

def test_recommendation():
    # Create a dummy dataset.
    data = {
        'imdb_title_id': ['id1', 'id2', 'id3'],
        'title': ['Movie A', 'Movie B', 'Movie C'],
        'genre': ['Action', 'Action', 'Action'],
        'year': [2000, 2001, 2002],
        'language': ['English', 'English', 'English'],
        'director': ['Dir A', 'Dir B', 'Dir C'],
        'writer': ['Wri A', 'Wri B', 'Wri C'],
        'production_company': ['PC A', 'PC B', 'PC C'],
        'actors': ['Actor A', 'Actor B', 'Actor C'],
        'country': ['Country A', 'Country A', 'Country A'],
        'description': ['Desc A', 'Desc B', 'Desc C'],
        'overview': ['Overview A', 'Overview B', 'Overview C'],
        'tagline': ['Tagline A', 'Tagline B', 'Tagline C']
    }
    df_dummy = pd.DataFrame(data)
    
    # Use 'Movie A' for testing.
    movie = 'Movie A'
    
    # Compute TF-IDF and cosine similarity on dummy data.
    X, df_text = compute_tfidf(df_dummy)
    sim_df = cosine_sim(X, df_text, movie)
    res = get_recommendations(df_text, sim_df)
    
    # Assert that recommendations were produced.
    assert not res.empty, "No recommendations returned."
    print("Test passed.")

if __name__ == '__main__':
    test_recommendation()

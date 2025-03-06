import pandas as pd
from html_template_functions import (
    load_content_data, filter_by_genre, filter_by_year, filter_by_language,
    remove_spaces, compute_tfidf, cosine_sim, get_recommendations
)

if __name__ == '__main__':
    # Load dataset
    df_all = load_content_data()
    
    # Use first movie as example
    movie = df_all['title'].iloc[0]
    
    # Apply filtering steps
    src = filter_by_genre(movie, df_all)
    src = filter_by_year(movie, src)
    src = filter_by_language(movie, src)
    src = remove_spaces(src)
    
    # Compute TF-IDF and cosine similarity
    X, df_text = compute_tfidf(src)
    sim_df = cosine_sim(X, df_text, movie)
    
    # Merge and print recommendations
    res = get_recommendations(df_text, sim_df)
    print(res)

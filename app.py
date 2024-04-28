import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load the CSV file
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    features = ['Product Name', 'Category', 'Product Specification']
    df['combined_features'] = df[features].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return df, cosine_sim

# Search function
def search_products(df, query):
    results = df[df['Product Name'].str.contains(query, case=False)]
    return results

# Recommendation function
def get_recommendations(product_id, cosine_sim, df, top_n=5):
    idx = df[df['Uniq Id'] == product_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    product_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[product_indices][['Uniq Id', 'Product Name', 'Category', 'Selling Price', 'Product Specification', 'Image', 'Product Url']]
    return recommendations

# Streamlit app
def main():
    st.title("Product Search")
    
    # Load the CSV file (Replace 'new_dataset.csv' with your actual file path)
    data, cosine_sim = load_data('new_dataset.csv')
    
    # Search bar
    search_query = st.text_input("Search for products", value="")
    
    # Filter the data based on the search query
    filtered_data = search_products(data, search_query)
    
    # Display the search results
    if len(filtered_data) > 0:
        st.subheader("Search Results")
        for _, row in filtered_data.iterrows():
            product_name = row['Product Name']
            unique_id = row['Uniq Id']
            product_url = row['Product Url']
            
            # Display product name, unique ID, and URL preview
            st.write(f"Product Name: {product_name} | Unique ID: {unique_id}")
            st.markdown(f"Product URL: [{product_url}]({product_url})")
            
            # Get recommendations for the product
            recommendations = get_recommendations(unique_id, cosine_sim, data)
            
            # Display recommendations
            if not recommendations.empty:
                st.subheader("Recommended Products")
                recommendations = recommendations.style.apply(lambda x: ["background-color: yellow" if x.name == unique_id else "" for _ in x], axis=1)
                st.dataframe(recommendations)
    else:
        st.warning("No products found.")

if __name__ == "__main__":
    main()
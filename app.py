import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Search function
def search_products(df, query):
    results = df[df['Product Name'].str.contains(query, case=False)]
    return results

# Streamlit app
def main():
    st.title("Product Search")

    # Load the CSV file (Replace 'data.csv' with your actual file path)
    data = load_data('new_dataset.csv')

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

    else:
        st.warning("No products found.")

if __name__ == "__main__":
    main()
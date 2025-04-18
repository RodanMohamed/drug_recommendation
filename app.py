import streamlit as st
import pandas as pd
import numpy as np
import pickle
import gzip

# Load the compressed similarity matrix
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# Load the compressed medicine dictionary
with gzip.open('medicine_dict.pkl.gz', 'rb') as f:
    medicine_dict = pickle.load(f)

# Convert dictionary to DataFrame
medicines = pd.DataFrame.from_dict(medicine_dict)

# Function to get recommendations based on a medicine name
def recommend(medicine_name):
    try:
        # Find the index of the medicine in the DataFrame
        idx = medicines[medicines['Drug_Name'].str.lower() == medicine_name.lower()].index[0]
    except IndexError:
        return "Medicine not found in the dataset."

    # Get the similarity scores for this medicine
    sim_scores = list(enumerate(similarity[idx]))

    # Sort the medicines by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Skip the first (self)

    # Get the recommended medicines
    recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in sim_scores]
    return recommended_medicines

# Streamlit app layout
st.title('💊 Drug Recommendation System')

# Input box for user to enter medicine name
medicine_name = st.text_input('Enter Medicine Name')

# Show recommendations when the button is clicked
if st.button('Get Recommendations'):
    if medicine_name:
        recommendations = recommend(medicine_name)
        if isinstance(recommendations, list):
            st.success('Recommended Drugs:')
            for drug in recommendations:
                st.write(f"🔹 {drug}")
        else:
            st.error(recommendations)
    else:
        st.warning("Please enter a medicine name.")

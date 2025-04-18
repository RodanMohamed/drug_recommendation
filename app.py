import streamlit as st
import pandas as pd
import numpy as np
import pickle
import gzip
import json

# Load the compressed models
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

with gzip.open('medicine_dict.pkl.gz', 'rb') as f:
    medicine_dict = pickle.load(f)

medicines = pd.DataFrame.from_dict(medicine_dict)

def recommend(medicine_name):
    try:
        idx = medicines[medicines['Drug_Name'].str.lower() == medicine_name.lower()].index[0]
    except IndexError:
        return []

    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    return [medicines.iloc[i[0]].Drug_Name for i in sim_scores]

# Streamlit app layout
st.title('💊 Drug Recommendation System')

# Input box for user to enter medicine name (standard input)
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

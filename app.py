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

# To make this accessible via HTTP requests (GET or POST)
import requests

def api_request(medicine_name):
    # Call the recommendation function and return the result as JSON
    recommendations = recommend(medicine_name)
    return json.dumps({'recommendations': recommendations})

# Handle GET/POST requests if needed
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def get_recommendations_api():
    data = request.get_json()
    medicine_name = data.get('medicine_name', '')
    recommendations = recommend(medicine_name)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)

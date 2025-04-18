from threading import Thread
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import gzip
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

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

# API route to handle the recommendation request
@app.route('/recommend', methods=['POST'])
def recommend_api():
    data = request.json
    medicine_name = data.get('medicine_name')
    
    if medicine_name:
        recommendations = recommend(medicine_name)
        if recommendations:
            return jsonify({'recommendations': recommendations}), 200
        else:
            return jsonify({'error': 'No recommendations found'}), 404
    else:
        return jsonify({'error': 'Medicine name is required'}), 400

# Streamlit app layout
def streamlit_app():
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

# Run Streamlit app in the background
def run_streamlit():
    import os
    os.system('streamlit run streamlit_app.py')

# Main function to run both Flask and Streamlit
if __name__ == '__main__':
    # Start Streamlit app in a background thread
    Thread(target=run_streamlit).start()

    # Run Flask API in the main thread
    app.run(debug=True, host='0.0.0.0', port=5000)

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import json
import os
from flask import Flask, request, jsonify

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "PASTE YOUR API KEY HERE"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Load SentenceTransformer for embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Sample SHL assessment data
assessments = [
    {
        "name": "Coding: Java",
        "url": "https://www.shl.com/solutions/products/product-catalog/coding-java",
        "description": "Tests Java programming skills for developers.",
        "duration": 30,
        "remote_support": "Yes",
        "adapting": "Yes",
        "test_type": ["Knowledge & Skills"]
    },
    {
        "name": "Python Programming",
        "url": "https://www.shl.com/solutions/products/product-catalog/python",
        "description": "Assesses proficiency in Python coding.",
        "duration": 25,
        "remote_support": "Yes",
        "adapting": "Yes",
        "test_type": ["Knowledge & Skills"]
    },
    {
        "name": "Occupational Personality Questionnaire",
        "url": "https://www.shl.com/solutions/products/product-catalog/opq",
        "description": "Evaluates personality traits for workplace fit.",
        "duration": 20,
        "remote_support": "Yes",
        "adapting": "No",
        "test_type": ["Competencies", "Personality & Behavior"]
    },
    {
        "name": "Verify G+",
        "url": "https://www.shl.com/solutions/products/product-catalog/verify-g",
        "description": "Measures general cognitive ability.",
        "duration": 36,
        "remote_support": "Yes",
        "adapting": "Yes",
        "test_type": ["Cognitive"]
    },
    {
        "name": "SQL Skills",
        "url": "https://www.shl.com/solutions/products/product-catalog/sql",
        "description": "Tests SQL query writing and database skills.",
        "duration": 20,
        "remote_support": "Yes",
        "adapting": "Yes",
        "test_type": ["Knowledge & Skills"]
    }
]

# Precompute embeddings
assessment_df = pd.DataFrame(assessments)
assessment_embeddings = embedder.encode(assessment_df["description"].tolist())

def extract_query_info(query):
    prompt = f"""
    Extract the following from the query:
    - Skills required (e.g., Java, Python)
    - Maximum duration (in minutes, if mentioned)
    - Test types (e.g., Cognitive, Personality, Skills)
    Query: {query}
    Return in JSON format.
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"skills": [], "duration": None, "test_types": []}

def recommend_assessments(query, max_duration=None, top_k=10):
    query_info = extract_query_info(query)
    skills = query_info.get("skills", [])
    max_duration = query_info.get("duration", max_duration)
    test_types = query_info.get("test_types", [])

    query_embedding = embedder.encode(query)
    similarities = cosine_similarity([query_embedding], assessment_embeddings)[0]
    assessment_df["similarity"] = similarities

    filtered_df = assessment_df.copy()
    if skills:
        filtered_df = filtered_df[filtered_df["description"].str.contains("|".join(skills), case=False, na=False)]
    if max_duration:
        filtered_df = filtered_df[filtered_df["duration"] <= max_duration]
    if test_types:
        filtered_df = filtered_df[filtered_df["test_type"].apply(lambda x: any(t in x for t in test_types))]

    recommendations = filtered_df.sort_values(by="similarity", ascending=False).head(top_k)
    return recommendations[[
        "name", "url", "duration", "remote_support", "adapting", "test_type", "description"
    ]].to_dict(orient="records")

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API is running"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    recommendations = recommend_assessments(query)
    return jsonify({"recommended_assessments": recommendations}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

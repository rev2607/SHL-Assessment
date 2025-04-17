# SHL Assessment Recommendation System Approach

## Overview
The goal was to build a web application that recommends SHL assessments based on natural language queries or job descriptions, leveraging Generative AI and vector search. The system processes queries, extracts key information, and matches them to assessments, returning up to 10 recommendations.

## Approach
1. **Data Collection**:
   - Simulated SHL assessment data from the product catalog (https://www.shl.com/solutions/products/product-catalog).
   - Includes name, URL, description, duration, remote_support, adapting, and test_type.

2. **Query Processing**:
   - Used Google Gemini API (e.g., gemini-1.5-flash or gemini-2.0-pro if supported) to extract skills, duration, and test types from queries.
   - Structured output in JSON for filtering.

3. **Recommendation Logic**:
   - Employed SentenceTransformer (`all-MiniLM-L6-v2`) for embeddings.
   - Used cosine similarity to rank assessments, filtered by skills, duration, and test types.

4. **Web Application**:
   - **Frontend**: Streamlit for an interactive UI.
   - **Backend**: Flask API with `/health` and `/recommend` endpoints.
   - Hosted in GitHub Codespaces with port forwarding.

5. **Evaluation**:
   - Tested with sample queries (e.g., "Java developers, 40 minutes").
   - Tracked accuracy informally; formal Mean Recall@3 and MAP@3 evaluation pending a benchmark set.

## Tools and Libraries
- **Generative AI**: Google Gemini API.
- **NLP**: SentenceTransformer, scikit-learn.
- **Web Framework**: Streamlit, Flask.
- **Data Handling**: Pandas.
- **Deployment**: GitHub Codespaces.

## Challenges and Solutions
- **Threading Issues**: Separated Flask and Streamlit into different files to avoid crashes.
- **Data Limitation**: Used simulated data; real data would require SHL API access.

## Future Improvements
- Integrate SHL’s API for real-time data.
- Use a larger dataset for better recommendations.
- Optimize with FAISS for scalability.

## Demo and Code
- **Demo URL**: (e.g., https://<your-codespace-id>-8501.app.github.dev)
- **API URL**: (e.g., http://localhost:5000/recommend)
- **GitHub**: (e.g., https://github.com/your-username/shl-assessment-recommender)
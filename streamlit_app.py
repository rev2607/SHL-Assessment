import streamlit as st
import requests

st.title("SHL Assessment Recommender")
query = st.text_area("Enter job description or query:")
max_duration = st.number_input("Max duration (minutes, optional):", min_value=0, value=0)
if st.button("Recommend"):
    if query:
        max_duration = max_duration if max_duration > 0 else None
        response = requests.post("http://localhost:5000/recommend", json={"query": query})
        if response.status_code == 200:
            recommendations = response.json()["recommended_assessments"]
            if recommendations:
                st.write("### Recommended Assessments")
                for rec in recommendations:
                    st.markdown(f"""
                    - **[{rec['name']}]({rec['url']})**
                    - Duration: {rec['duration']} minutes
                    - Remote Testing: {rec['remote_support']}
                    - Adaptive/IRT: {rec['adapting']}
                    - Test Type: {', '.join(rec['test_type'])}
                    - Description: {rec['description']}
                    """)
            else:
                st.write("No assessments match your criteria.")
        else:
            st.write(f"Error: {response.status_code} - {response.text}")
    else:
        st.write("Please enter a query.")
import streamlit as st
import requests
import pandas as pd

API_URL = "https://shl-recommendation-dc8j.onrender.com"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")


st.title("SHL Intelligent Recommender")
st.markdown("""
This tool helps you find the perfect **SHL Assessments** for your job descriptions.
It uses AI to balance **Hard Skills** (e.g., Java, Python) with **Soft Skills** (e.g., Leadership, Collaboration).
""")


with st.form("search_form"):
    query = st.text_area("Enter Job Description or Query:", height=100, 
                         placeholder="Example: Looking for a Java Developer who can lead a team and has good communication skills.")
    submitted = st.form_submit_button("Find Assessments")

if submitted and query:
    with st.spinner("Analyzing requirements & searching catalog..."):
        try:
          
            payload = {"query": query}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                results = response.json()
                
                if results:
                    st.success(f"Found {len(results)} relevant assessments:")
                    
                    
                    df = pd.DataFrame(results)
                    
                    
                    st.dataframe(
                        df,
                        column_config={
                            "URL": st.column_config.LinkColumn("Assessment Link"),
                            "Assessment Name": st.column_config.TextColumn("Assessment Name", width="medium")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning("No specific assessments found. Try refining your query.")
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Is `api.py` running?")
        except Exception as e:
            st.error(f"An error occurred: {e}")
import os
import json
from google import genai
from google.genai import types
import trafilatura
import streamlit as st

def analyze_competitor(competitor_name):
    GOOGLE_API_KEY = os.environ.get('GEMINI_KEY')
    if not GOOGLE_API_KEY: return {"error": "GEMINI_KEY missing"}
    
    client = genai.Client(api_key=GOOGLE_API_KEY)
    url = f"https://en.wikipedia.org/wiki/{competitor_name.replace(' ', '_')}"
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded) or "" if downloaded else ""
    
    if not text: return {"error": "No data found"}

    prompt = f"Analyze {competitor_name} based on this data: {text[:8000]}. Return JSON with keys: brands, campaigns, features_pricing."
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(category='HATE_SPEECH', threshold='BLOCK_NONE'),
                    types.SafetySetting(category='HARASSMENT', threshold='BLOCK_NONE'),
                    types.SafetySetting(category='DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
                    types.SafetySetting(category='SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
                ]
            )
        )
        return json.loads(response.text)
    except Exception as e: return {"error": str(e)}

st.title("Competitor Intelligence Agent")
name = st.text_input("Competitor Name")
if st.button("Analyze"):
    if name:
        res = analyze_competitor(name)
        st.json(res)
    else:
        st.warning("Enter a name")

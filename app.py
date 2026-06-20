
import os
import json
from google import genai
import trafilatura
import streamlit as st

# Existing analyze_competitor function (copied here for self-contained app.py)
def analyze_competitor(competitor_name):
    GOOGLE_API_KEY = os.environ.get('GEMINI_KEY')

    if not GOOGLE_API_KEY:
        return {"error": "GEMINI_KEY environment variable not set. Please set your API key in Colab secrets or environment variables."}

    client = genai.Client(api_key=GOOGLE_API_KEY)

    research_targets = [
        "main brand names and sub-brands",
        "recent marketing campaigns",
        "pricing plans and key product features"
    ]

    combined_text = ""
    for target in research_targets:
        url = f"https://en.wikipedia.org/wiki/{competitor_name.replace(' ', '_')}"
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            combined_text += trafilatura.extract(downloaded) or ""
            if len(combined_text) > 8000: 
                combined_text = combined_text[:8000]
                break

    if not combined_text:
        return {"error": f"Could not extract any meaningful text for {competitor_name} from Wikipedia."}

    prompt = f"""
    You are an expert market research analyst.
    Analyze the following raw web data about {competitor_name} and extract:
    1. Main brand names and sub-brands
    2. Recent marketing campaigns
    3. Pricing plans and key product features

    Provide your response strictly in a clean JSON format with these exact keys:
    "brands", "campaigns", "features_pricing".

    Raw Web Data:
    {combined_text}
    """
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE',
            }
        )
        response_text = response.text
    except Exception as e:
        return {"error": f"Gemini API call failed: {e}"}

    try:
        return json.loads(response_text)
    except Exception as e:
        return {"error": "Could not parse JSON from API response", "raw_output": response_text, "exception": str(e)}


# --- Streamlit Web Interface ---
st.set_page_config(page_title="Competitor Intelligence Agent", layout="centered")

st.title("Competitor Intelligence Agent")
st.write("Enter a competitor name below to get an analysis of their brands, marketing campaigns, and features/pricing.")

competitor_name = st.text_input("Enter Competitor Name:", placeholder="e.g., Apple Inc., Samsung")

if st.button("Analyze"):
    if competitor_name:
        with st.spinner(f"Analyzing {competitor_name}..."):
            analysis_result = analyze_competitor(competitor_name)

        st.subheader(f"Analysis for {competitor_name}")
        if "error" in analysis_result:
            st.error(f"Error: {analysis_result['error']}")
            if "raw_output" in analysis_result:
                st.code(analysis_result['raw_output'], language='json')
            if "exception" in analysis_result:
                st.exception(analysis_result['exception'])
        else:
            st.json(analysis_result)
    else:
        st.warning("Please enter a competitor name to analyze.")

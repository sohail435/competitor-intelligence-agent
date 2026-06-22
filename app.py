import os
import json
import requests
from google import genai
from google.genai import types
import trafilatura
import streamlit as st


def get_secret(name):
    value = os.environ.get(name)
    if value:
        return value

    try:
        return st.secrets[name]
    except (FileNotFoundError, KeyError):
        return ""


def build_mock_competitor_report(competitor_name):
    name = competitor_name.strip() or "Selected Competitor"

    return {
        "brands": [
            {
                "name": name,
                "positioning": "Primary brand used for broad market visibility and customer acquisition.",
                "sub_brands": [
                    f"{name} Core",
                    f"{name} Pro",
                    f"{name} Enterprise"
                ]
            }
        ],
        "campaigns": [
            {
                "name": f"{name} digital awareness campaign",
                "timeframe": "Recent 12 months (mock)",
                "channels": ["search", "social", "content marketing"],
                "message": "Emphasizes product reliability, speed to value, and competitive differentiation."
            },
            {
                "name": f"{name} customer retention push",
                "timeframe": "Recent 12 months (mock)",
                "channels": ["email", "webinars", "case studies"],
                "message": "Highlights customer outcomes, feature adoption, and upgrade paths."
            }
        ],
        "features_pricing": {
            "summary": "Mock pricing model with entry, professional, and enterprise tiers.",
            "tiers": [
                {
                    "name": "Starter",
                    "price": "$19/user/month",
                    "features": ["basic dashboards", "standard support", "limited exports"]
                },
                {
                    "name": "Professional",
                    "price": "$49/user/month",
                    "features": ["advanced analytics", "team workflows", "priority support"]
                },
                {
                    "name": "Enterprise",
                    "price": "custom",
                    "features": ["SSO", "custom integrations", "dedicated account management"]
                }
            ]
        },
        "mock_notice": "Mock fallback generated because GEMINI_KEY is not configured."
    }


def fetch_tavily_data(query):
    """Helper to fetch search results from Tavily API."""
    api_key = get_secret('TAVILY_API_KEY')
    if not api_key: return ""
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 5
    }
    try:
        response = requests.post(url, json=payload)
        results = response.json().get('results', [])
        return "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in results])
    except:
        return ""

def analyze_competitor(competitor_name):
    gemini_key = get_secret('GEMINI_KEY')
    if not gemini_key: return build_mock_competitor_report(competitor_name)

    client = genai.Client(api_key=gemini_key)

    # 1. Wikipedia Data
    wiki_url = f"https://en.wikipedia.org/wiki/{competitor_name.replace(' ', '_')}"
    wiki_text = trafilatura.extract(trafilatura.fetch_url(wiki_url)) or ""

    # 2. Real-time Data via Tavily
    search_query = f"{competitor_name} latest news marketing pricing 2024 2025"
    search_text = fetch_tavily_data(search_query)

    combined_data = f"WIKIPEDIA CONTENT:\n{wiki_text[:4000]}\n\nWEB SEARCH CONTENT:\n{search_text[:4000]}"

    prompt = f"""
    Analyze {competitor_name} using the provided data. Extract:
    1. Brands and sub-brands
    2. Recent marketing campaigns (last 12 months)
    3. Current pricing and key features

    Return strictly JSON with keys: brands, campaigns, features_pricing.
    Data:
    {combined_data}
    """

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                safety_settings=[types.SafetySetting(category=c, threshold='BLOCK_NONE') for c in ['HATE_SPEECH', 'HARASSMENT', 'DANGEROUS_CONTENT', 'SEXUALLY_EXPLICIT']]
            )
        )
        return json.loads(response.text)
    except Exception as e: return {"error": str(e)}

def main():
    st.set_page_config(page_title="Competitor Agent v2.0")
    st.title("Competitor Intelligence Agent (Live Web Access)")
    name = st.text_input("Competitor Name")
    if st.button("Analyze"):
        if name:
            with st.spinner("Searching web and analyzing..."):
                res = analyze_competitor(name)
                st.json(res)
        else:
            st.warning("Enter a name")


if __name__ == "__main__":
    main()

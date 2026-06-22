
# Competitor Intelligence Agent

This project provides a Streamlit app (`app.py`) to analyze competitor information using the Gemini API and `trafilatura` for web content extraction.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Google Gemini API Key:**
    Obtain an API key from Google AI Studio and set it as an environment variable named `GEMINI_KEY`.
    On Streamlit Community Cloud, add `GEMINI_KEY` in the app's secrets settings.
    If `GEMINI_KEY` is not configured, the app displays a realistic mock competitor report so the UI remains usable.

3.  **Optional Tavily API Key:**
    Set `TAVILY_API_KEY` as an environment variable or Streamlit secret to include live web search results.

## Usage

To run the competitor analysis:

```bash
streamlit run app.py
```

Enter a competitor name in the Streamlit app and click **Analyze**.

## `analyze_competitor` Function

The core function `analyze_competitor(competitor_name)` takes a competitor's name as input and returns a JSON object with extracted information on brands, marketing campaigns, and product features/pricing.

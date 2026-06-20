
# Competitor Intelligence Agent

This project provides a Python script (`app.py`) to analyze competitor information using the Google Gemini API and `trafilatura` for web content extraction. It features a Streamlit web interface for interactive use.

## Setup

1.  **Dependencies:** Install the required packages using `pip install -r requirements.txt`.
2.  **API Key:** Obtain a Google Gemini API key from Google AI Studio and set it as an environment variable named `GEMINI_KEY`. If deploying to Streamlit Cloud, add it as a secret.

## Usage

To run the Streamlit application:

```bash
streamlit run app.py
```

If running in a Colab environment and you need a public URL, you can use `npx localtunnel`:

```bash
nohup python -m streamlit run app.py & npx localtunnel --port 8501
```

## `analyze_competitor` Function

The core function `analyze_competitor(competitor_name)` takes a competitor's name as input and returns a JSON object with extracted information on brands, marketing campaigns, and product features/pricing.

## Deployment

This application can be deployed to Streamlit Cloud by connecting your GitHub repository. Ensure `app.py` and `requirements.txt` are in the root of your repository.

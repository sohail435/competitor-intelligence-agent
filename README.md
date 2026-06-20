
# Competitor Intelligence Agent

This project provides a Python script (`app.py`) to analyze competitor information using the Gemini API and `trafilatura` for web content extraction.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Google Gemini API Key:**
    Obtain an API key from Google AI Studio and set it as an environment variable named `GEMINI_KEY`.
    In Google Colab, you can add this to the secrets manager under the '🔑' icon.

## Usage

To run the competitor analysis:

```bash
python app.py
```

The `app.py` script includes an example analysis for 'Apple Inc.'

## `analyze_competitor` Function

The core function `analyze_competitor(competitor_name)` takes a competitor's name as input and returns a JSON object with extracted information on brands, marketing campaigns, and product features/pricing.

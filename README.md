# Intelligence Evaluations Dashboard

A web application to display intelligence evaluation scores for open-source AI models, similar to the structure on [artificialanalysis.ai/models/open-source](https://artificialanalysis.ai/models/open-source).

## Features

- 📊 Display model performance across multiple benchmarks (MMLU, AALCR, SciCode, τ²-Bench, Telecom, etc.)
- 🔍 Search and filter models
- 📈 Color-coded scores (high/medium/low performance)
- 🎨 Modern, responsive UI
- 🔄 Refresh data functionality

## Project Structure

```
Test_AA/
├── index.html          # Main web interface
├── styles.css          # Styling
├── app.js             # Frontend JavaScript
├── data_fetcher.py    # Data fetching script (sample data)
├── api_client.py      # API client for artificialanalysis.ai
├── web_scraper.py     # Web scraper for the website
├── evaluations_data.json  # Data file (generated)
└── README.md          # This file
```

## Setup

1. **Install dependencies:**
   ```bash
   pip3 install requests beautifulsoup4
   ```

2. **Fetch data:**
   ```bash
   # Try API first (recommended)
   python3 api_client.py
   
   # Or try web scraping (for JavaScript-rendered pages)
   python3 web_scraper.py
   
   # Or use Selenium scraper (requires ChromeDriver)
   pip install selenium
   python3 selenium_scraper.py
   
   # Or use sample data (fallback)
   python3 data_fetcher.py
   ```

3. **Open the web interface:**
   - **Option 1:** Use the included server (recommended):
     ```bash
     python3 server.py
     ```
     This will automatically open your browser
   
   - **Option 2:** Use Python's built-in server:
     ```bash
     python3 -m http.server 8000
     ```
     Then visit `http://localhost:8000`
   
   - **Option 3:** Simply open `index.html` directly in your browser

## API Key

Your API key is configured in the scripts:
- `api_client.py`: `aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT`
- `data_fetcher.py`: `aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT`

## Benchmarks Included

- **MMLU** - Massive Multitask Language Understanding
- **AALCR** - AALCR Benchmark
- **SciCode** - Scientific Code Understanding
- **τ²-Bench** - Tau Squared Benchmark
- **Telecom** - Telecom Benchmark
- **HellaSwag** - HellaSwag Benchmark
- **ARC** - AI2 Reasoning Challenge
- **TruthfulQA** - TruthfulQA Benchmark
- **GSM8K** - Grade School Math 8K
- **Winogrande** - Winogrande Benchmark

## Data Format

The `evaluations_data.json` file follows this structure:

```json
{
  "benchmarks": [
    {
      "id": "mmlu",
      "name": "MMLU",
      "full_name": "Massive Multitask Language Understanding"
    }
  ],
  "models": [
    {
      "id": "deepseek-v3.2",
      "name": "DeepSeek V3.2",
      "provider": "DeepSeek",
      "scores": {
        "mmlu": 0.85,
        "aalcr": 0.69,
        "scicode": 0.42
      }
    }
  ]
}
```

## Usage

1. **View Evaluations:**
   - Open `index.html` in your browser
   - The table displays all models with their scores

2. **Search Models:**
   - Use the search box to filter models by name or provider

3. **Refresh Data:**
   - Click the "Refresh Data" button to reload from `evaluations_data.json`

## Getting Real Data

To get actual scores from artificialanalysis.ai:

1. **API Method:**
   - Update `api_client.py` with correct API endpoints if they differ
   - Run `python3 api_client.py`

2. **Scraping Method:**
   - If the website uses JavaScript rendering, you may need Selenium/Playwright
   - Run `python3 web_scraper.py`

3. **Manual Method:**
   - Manually update `evaluations_data.json` with real scores
   - The web interface will automatically display the updated data

## Customization

- **Add more benchmarks:** Edit the benchmarks list in `data_fetcher.py` or `evaluations_data.json`
- **Add more models:** Add entries to the models array in `evaluations_data.json`
- **Styling:** Modify `styles.css` to change colors, fonts, or layout
- **Functionality:** Extend `app.js` for additional features

## Notes

- The API endpoints may require authentication or have different URLs
- If the website structure changes, update `web_scraper.py` accordingly
- Scores are displayed as percentages (0.85 = 85%)
- Color coding: Green (≥80%), Yellow (60-79%), Red (<60%)

## License

This project is for educational and evaluation purposes.


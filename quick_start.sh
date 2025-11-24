#!/bin/bash
# Quick start script for Intelligence Evaluations Dashboard

echo "=========================================="
echo "Intelligence Evaluations Dashboard"
echo "=========================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Try to fetch data
echo "Step 1: Fetching data..."
if python3 api_client.py 2>/dev/null; then
    echo "✓ Data fetched from API"
elif python3 web_scraper.py 2>/dev/null; then
    echo "✓ Data scraped from website"
else
    echo "⚠ Using sample data"
    python3 data_fetcher.py
fi

echo ""
echo "Step 2: Starting web server..."
echo "The dashboard will open in your browser automatically."
echo "Press Ctrl+C to stop the server."
echo ""

# Start server
python3 server.py





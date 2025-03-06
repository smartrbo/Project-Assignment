from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# YouTube API Key (Replace with your own key)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Function to fetch YouTube videos
def get_youtube_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 5
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("items", [])

# Function to fetch Amazon product details (Placeholder)
def get_amazon_products(query):
    return [
        {"title": "Sample Amazon Product 1", "price": "$20"},
        {"title": "Sample Amazon Product 2", "price": "$35"}
    ]  # Replace with real Amazon API results

@app.route('/', methods=['GET', 'POST'])
def home():
    youtube_results = []
    amazon_results = []
    
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        youtube_results = get_youtube_videos(search_query)
        amazon_results = get_amazon_products(search_query)
    
    return render_template("index.html", youtube_results=youtube_results, amazon_results=amazon_results)

if __name__ == "__main__":
    app.run(debug=True)
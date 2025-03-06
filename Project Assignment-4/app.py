from flask import Flask, render_template, request

app = Flask(__name__)

# Sample content database (can be replaced with a real database)
content_db = {
    "technology": ["AI Trends in 2025", "Latest Python Updates", "Cloud Computing Basics"],
    "sports": ["FIFA World Cup Highlights", "Best NBA Players in 2024", "Olympic Records"],
    "movies": ["Top Sci-Fi Movies", "Best Animated Films", "Classic Horror Movies"],
    "music": ["Top 10 Rock Albums", "Best Classical Composers", "Upcoming Pop Concerts"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_preference = request.form.get("category")
        recommendations = content_db.get(user_preference, ["No recommendations available."])
        return render_template("recommendations.html", category=user_preference, recommendations=recommendations)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

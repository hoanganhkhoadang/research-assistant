import re

from flask import Flask, render_template, request

from sources_only import collect_sources

app = Flask(__name__)

# Function to detect if user entered a question
def is_question(topic: str) -> bool:
    """
    Returns True if the input looks like a direct question.
    Checks if it starts with question words like who, what, how, why, when, etc.
    """
    topic = topic.strip().lower()
    return bool(re.match(r"^(who|what|how|why|when|where)\b", topic))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    topic = ""
    warning = ""

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()

        if is_question(topic):
            warning = "⚠️ Please enter a research topic, not a direct question."
        elif topic:
            results = collect_sources(topic)
            if not results:
                warning = "No sources found. Try a different research topic."

    return render_template("index.html", topic=topic, results=results, warning=warning)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # Safe fallback

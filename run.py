from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import random, string

app = Flask(__name__)
CORS(app)

# In-memory database (Dictionary)
url_db = {}

# Function to generate a short key
def generate_short_key(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    short_key = generate_short_key()
    url_db[short_key] = original_url

    short_url = f"http://localhost:5000/{short_key}"  # Change this for production
    return jsonify({"shortened": short_url})

# Redirect to the original URL
@app.route('/<short_key>')
def redirect_to_original(short_key):
    original_url = url_db.get(short_key)
    if original_url:
        return redirect(original_url, code=302)
    return "URL not found", 404

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)

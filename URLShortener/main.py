from . import app, db  # Import them from __init__.py
from flask import request, jsonify, redirect, render_template


# Import models here after db creation


# Function to generate a short key
def generate_short_key(length=6):
    while True:
        short_key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if short_key not in db:
            return short_key


# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    short_key = generate_short_key()
    db[short_key] = original_url

    short_url = f"http://localhost:5000/{short_key}"  # Change this for production
    return jsonify({"shortened": short_url})

# Route to unshorten a URL
@app.route('/unshorten', methods=['GET'])
def unshorten_url():
    
    
    shortened_url = request.args.get("url")

    if not shortened_url:
        return jsonify({"error": "No URL provided"}), 400
    
    short_key = shortened_url.split('/')[-1]
    original_url = db.get(short_key) # unshortened url

    return jsonify({"unshortened": original_url})


# Redirect to the original URL
@app.route('/<short_key>')
def redirect_to_original(short_key):
    
    original_url = db.get(short_key)

    

    if original_url:
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        return redirect(original_url)
    else:
        return render_template('errorpage.html')
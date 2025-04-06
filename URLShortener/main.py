import random
import string
from .db import db
  # Import them from __init__.py
from .models import URL  # Import the URL model
from flask import request, jsonify, redirect, render_template
from flask import Blueprint
from ..log.debug_print import dprint

main_bp = Blueprint('main', __name__)



# Function to generate a short key
# TODO: change the logic to use hashing -> which can make no collision
def generate_short_key(length=6):
    while True: # avoid collision
        short_key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Check if short_key already exists in database
        existing_url = db.session.execute(db.select(URL).filter_by(short_url=short_key)).first()
        if not existing_url:
            dprint(f"new key: {short_key}")
            return short_key


# Route to shorten a URL
@main_bp.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    # Check if URL already exists
    #### Not needed: shortened URLs must be unique for security.
    # existing_url = db.session.execute(db.select(URL).filter_by(original_url=original_url)).first()
    # if existing_url:
    #     short_key = existing_url[0].short_url
    # else:
    dprint(f"Just got a url....: {original_url}")
    short_key = generate_short_key()
    new_url = URL(original_url=original_url, short_url=short_key)
    db.session.add(new_url)
    db.session.commit()
    dprint("successfully saved to database")

    short_url = f"http://localhost:5000/{short_key}"  # Change this when production
    return jsonify({"shortened": short_url})

# Route to unshorten a URL
@main_bp.route('/unshorten', methods=['GET'])
def unshorten_url():
    shortened_url = request.args.get("url")

    if not shortened_url:
        dprint("No URL provided")
        return jsonify({"error": "No URL provided"}), 400
    
    short_key = shortened_url.split('/')[-1]

    dprint(f"Just got a short url....: {shortened_url}")
    url_record = db.session.execute(db.select(URL).filter_by(short_url=short_key)).first()
    
    if url_record:
        original_url = url_record[0].original_url
        dprint(f"Found original url for {short_key}: {original_url}")
        return jsonify({"unshortened": original_url})
    else:
        return jsonify({"error": "URL not found"}), 404


# Redirect to the original URL
@main_bp.route('/<short_key>')
def redirect_to_original(short_key):
    url_record = db.session.execute(db.select(URL).filter_by(short_url=short_key)).first()
    

    dprint(f"I have to redirect using: {short_key}")
    

    if url_record:
        dprint(f"original url fetched from database: {url_record[0].original_url}")
        original_url = url_record[0].original_url
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url # `original_url` is not overriden 
                                                    # because it is in the same scope as above.
                                                    # prepend http:// because most sites automatically
                                                    # redirect to https://.
                                                    # TODO: make this more robust
        dprint(f"Redirecting to: {original_url}")
        return redirect(original_url)
    else:
        dprint("original url not found.... sending to error page")
        return redirect('http://localhost:5500/URLShortener/templates/errorpage.html')
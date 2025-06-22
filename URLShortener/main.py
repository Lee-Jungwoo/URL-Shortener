import random
import string
from .db import db
from .models import URL  # Import the URL model
from flask import request, jsonify, redirect, current_app, render_template, url_for
from flask import Blueprint
from log.debug_print import dprint




main_bp = Blueprint('main', __name__, url_prefix='/api')
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
        

@main_bp.route('/ready')
def link_ready(short_url=None):
    """
    Render a template to show the shortened URL.
    """
    dprint("Rendering link-ready template")
    short_url = request.args.get('short_url')
    if not short_url:
        return jsonify({"error": "No short URL provided"}), 400
    return render_template("link-ready.html", short_url=short_url)



# Route to shorten a URL
@main_bp.route('/shorten', methods=['GET'])
def shorten_url():
    
    
    original_url = request.args.get("url")
    custom_key = request.args.get("custom_key")
    
    if not original_url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Get the real IP address from X-Forwarded-For header if behind a proxy
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    dprint(f"Just got a url....: {original_url}\nfrom IP: {ip_addr}")

    if custom_key:
        db_key = db.session.execute(db.select(URL).filter_by(short_url=custom_key)).first()
        if db_key:
            return jsonify({"error": "Custom key already exists"}), 400
        else:
            dprint(f"Custom key provided: {custom_key}")
            short_key = custom_key
    else:
        dprint("No custom key provided")
        dprint("Generating a new short key...")
        short_key = generate_short_key()
        dprint(f"Generated short key: {short_key}")
    
    
    new_url = URL(original_url=original_url, short_url=short_key)
    db.session.add(new_url)
    db.session.commit()
    dprint("successfully saved to database")

    short_url = f"{current_app.config['REDIRECT_URL']}/{short_key}"  # Change this when production
    return redirect(url_for('main.link_ready', short_url=short_url))



# Route to unshorten a URL
@main_bp.route('/unshorten', methods=['GET'])
def unshorten_url():
    shortened_url = request.args.get("url")

    if not shortened_url:
        dprint("No URL provided")
        return jsonify({"error": "No URL provided"}), 400
    
    short_key = shortened_url.split('/')[-1]

    # Get the real IP address from X-Forwarded-For header if behind a proxy
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    dprint(f"Just got a short url....: {shortened_url}\nfrom IP: {ip_addr}")
    url_record = db.session.execute(db.select(URL).filter_by(short_url=short_key)).first()
    
    if url_record:
        original_url = url_record[0].original_url
        dprint(f"Found original url for {short_key}: {original_url}")
        return jsonify({"unshortened": original_url})
    else:
        return jsonify({"error": "URL not found"}), 404



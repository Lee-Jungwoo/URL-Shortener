import random
import string
from .db import db
from .models import URL  # Import the URL model
from flask import request, jsonify, redirect, current_app
from flask import Blueprint
from log.debug_print import dprint




redirect_bp = Blueprint('redirect', __name__)






# Redirect to the original URL
@redirect_bp.route('/<short_key>')
def redirect_to_original(short_key):
    url_record = db.session.execute(db.select(URL).filter_by(short_url=short_key)).first()
    

    dprint(f"Should redirect using: {short_key}")
    

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
        return redirect(f"{current_app.config['CLIENT_URL']}/URLShortener/templates/errorpage.html")
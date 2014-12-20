from flask.ext.babel import format_datetime, format_date
from flask import render_template
from datetime import datetime
from urllib.parse import quote
import os
import json

def timesince(dt, default="Just now."):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

def local_date(datestamp):
    return format_date(datestamp)

def percent_escape(string):
    return quote(string, '')

def local_date_time(datestamp):
    if datestamp:
        return format_datetime(datestamp)

# Use a factory to set the app variable.
def get_autoincluded_assets(app):
    def func(**kwargs):
        fn = os.path.realpath('./Application/static/vendor/autoinclude.json')
        data = None
        with open(fn, 'r') as f:
            data = json.loads(f.read())

        if data and 'scripts' in data and 'stylesheets' in data:
            with app.app_context():
                return render_template('_boilerplate/sources.html', 
                    scripts=data['scripts'], 
                    stylesheets=data['stylesheets'])

    return func

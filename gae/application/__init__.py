# raku-tabi application/__init__.py

import urllib

from flask import Flask   #, request

from config import Config, Const


# Flask
app = Flask(__name__)
app.config.from_object(Config)


# Jinja
app.jinja_env.globals.update(Const.__dict__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def _intcomma(num):
    return "{:,}".format(num) if num else num


def _urlquote(str, safe="/"):
    return urllib.parse.quote(str, safe=safe) if str else None


app.jinja_env.filters['intcomma'] = _intcomma
app.jinja_env.filters['urlquote'] = _urlquote


# views
from . import views

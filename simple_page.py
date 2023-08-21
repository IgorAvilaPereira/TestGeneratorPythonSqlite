from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates', static_folder="static")

@simple_page.route('/')
def show():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        return "agora"
        # abort(404)
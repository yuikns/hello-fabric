from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

example = Blueprint('example', __name__, template_folder='templates')


@example.route('/', defaults={'page': 'index'})
@example.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        return render_template("pages/404.html")

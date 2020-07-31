from flask import Blueprint, render_template, request, redirect
from .extensions import db
from .models import Url

shorturl = Blueprint('shorturl', __name__, template_folder='templates')

@shorturl.route('/')
def index():
    return render_template('index.html')

@shorturl.route('/<short_url>')
def redirect_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.long_url)

@shorturl.route('/', methods=['POST'])
def create():
    long_url = request.form['long_url']
    short_url = request.form['short_url']
    
    # error checking
    if db.session.query(db.exists().where(Url.short_url == short_url)).scalar():
        return render_template('url_existed.html')

    url = Url(long_url=long_url, short_url=short_url)
    db.session.add(url)
    db.session.commit()
    return render_template('url_created.html', new_url=url.short_url)

@shorturl.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

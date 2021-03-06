# -*- coding: utf-8 -*-
"""Simple Flask personal web page."""
import os
from os import path
import re
import traceback
import logging
import logging.config

from flask import Flask, render_template, request, send_from_directory, redirect
from flask_babel import Babel
from jinja2.exceptions import TemplateNotFound

from flask import Flask

app = Flask(__name__, static_folder = 'static')
application = app
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400
app.config.from_pyfile('../flask.cfg')
babel = Babel(app)

logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), '../log.cfg'))
log = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run()

from smtp import SimpleSMTP

try:
    email
except NameError:
    email = SimpleSMTP(os.path.join(app.root_path, '../smtp.cfg'))


MULTILANGUAGE_LANGUAGES = ['hr', 'en']
MULTILANGUAGE_TEMPLATES = ['cv']

@babel.localeselector
def get_locale():
    """Return current locale as string."""
    lang = request.args.get('lang')
    if lang is not None:
        return lang
    for x in list(request.accept_languages.values()):
        lang = x.replace('_', '-').split('-')[0]
        if lang in MULTILANGUAGE_LANGUAGES:
            return lang
    return MULTILANGUAGE_LANGUAGES[0]

def link_suffix():
    lang = request.args.get('lang')
    if lang is None:
        return ''
    return '?lang=' + get_locale()

def my_router(path, missing, lang):
    m = re.search('^/?(.*[^/])/?$', path)
    if m is None:
        return ''

    clean_path = m.group(1)

    m = re.search('^(.*/)?([^_][^/]+)?$', clean_path)
    if m is None:
        return missing
    folder = m.group(1)
    if folder is None:
        folder = ''
    name = m.group(2)

    if lang is None:
        lang = 'en'

    if name in MULTILANGUAGE_TEMPLATES:
        return folder + '_' + name + '_' + lang
    return clean_path

@app.route('/', defaults = {'path': 'cover'}, methods = ['GET'])
@app.route('/<path:path>', methods = ['GET'])
def my_general_route(path):
    """Path redirect mechanism."""
    return render_template(
        my_router(path, '_404', get_locale()) + '.html',
        lang = get_locale(),
        link_suffix = link_suffix())


@app.route('/favicon.ico')
def favicon():
    """Return favicon resource."""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'icon.png',
        mimetype = 'image/png')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/site.webmanifest')
def static_from_root():
    """Custom static resources."""
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/send', methods = ['POST'])
def send_message():
    """Send mail message from POST data.

    POST attributes:
        name - name of the sender,
        title - message title,
        email - email of the sender,
        message - the message itself."""

    email.send_mail(
        'isikacek@gmail.com',
        'isikacek@gmail.com',
        'webmsg: ' + request.form['name'] + ' - ' + request.form['title'],
        request.form['message'] + '\n\n' + request.form['email'])
    return ''


@app.errorhandler(TemplateNotFound)
@app.errorhandler(404)
def bad_turn(path):
    """Redirect to 404 page."""
    return render_template('_404.html',
        lang = get_locale(),
        link_suffix = link_suffix())


@app.errorhandler(Exception)
@app.errorhandler(500)
def server_error(error):
    """Log error and redirect to 500 page."""
    #print(traceback.format_exc())
    log.exception(error)
    return render_template('_500.html',
        lang = get_locale(),
        link_suffix = link_suffix())

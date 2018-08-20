# -*- coding: utf-8 -*-
"""Simple Flask personal web page."""
import os
import re
#import logging
#import logging.config

from flask import Flask, render_template, request, send_from_directory, redirect
from flask_babel import Babel
from jinja2.exceptions import TemplateNotFound

try:
    from gae import send_mail
except ImportError:
    from no_env import send_mail

from isikacek import app, babel#, log

MULTILANGUAGE_TEMPLATES = ['cv']

#app.config.from_pyfile('flask.cfg')
#babel = Babel(app)

#logging.config.fileConfig('log.cfg')
#log = logging.getLogger(__name__)


@babel.localeselector
def get_locale():
    """Return current locale as string."""
    lang = request.args.get('lang')
    if lang is not None:
        return lang
    return request.accept_languages.best_match(['hr', 'en'])

def link_suffix():
    lang = request.args.get('lang')
    if lang is None:
        return ''
    return '/?lang=' + get_locale()

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

    if name in MULTILANGUAGE_TEMPLATES:
        return folder + '_' + name + '_' + lang
    return clean_path


@app.route('/', defaults={'path': 'cover'}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def my_general_route(path):
    """Path redirect mechanism."""
    return render_template(
        my_router(path, '_404', get_locale()) + '.html',
        lang=get_locale(),
        link_suffix=link_suffix())


@app.route('/favicon.ico')
def favicon():
    """Return favicon resource."""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'icon.png',
        mimetype='image/png')


@app.route('/contact', methods=['POST'])
def send_message():
    """Send mail message from POST data.

    POST attributes:
        name - name of the sender,
        title - message title,
        email - email of the sender,
        message - the message itself."""

    send_mail(
        'isikacek-web',
        'isikacek@gmail.com',
        '' + request.form['name'] + ' - ' + request.form['title'],
        request.form['message'] + '\n\n' + request.form['email'])
    return redirect('/contact')


@app.errorhandler(TemplateNotFound)
@app.errorhandler(404)
def bad_turn(path):
    """Redirect to 404 page."""
    return render_template('_404.html',
        lang=get_locale(),
        link_suffix=link_suffix())


@app.errorhandler(Exception)
@app.errorhandler(500)
def server_error(error):
    """Log error and redirect to 500 page."""
    #log.exception(error)
    return render_template('_500.html',
        lang=get_locale(),
        link_suffix=link_suffix())

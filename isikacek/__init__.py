
from flask import Flask
from flask_babel import Babel
#import logging
#import logging.config

app = Flask(__name__, static_folder = 'static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400

app.config.from_pyfile('../flask.cfg')
babel = Babel(app)

#logging.config.fileConfig('log.cfg')
#log = logging.getLogger(__name__)

import isikacek.views


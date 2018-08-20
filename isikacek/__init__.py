
from flask import Flask
from flask_babel import Babel
#import logging
#import logging.config

app = Flask(__name__)

app.config.from_pyfile('../flask.cfg')
babel = Babel(app)

#logging.config.fileConfig('log.cfg')
#log = logging.getLogger(__name__)

import isikacek.views

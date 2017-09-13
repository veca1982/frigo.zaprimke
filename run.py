# run.py

import os
import sys

from app import create_app


config_name = os.getenv('FLASK_CONFIG')
#config_name = 'production'
app = create_app(config_name)
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    app.run()
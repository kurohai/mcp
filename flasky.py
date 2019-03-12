#!/usr/bin/env python


import os

from flask_migrate import Migrate
from mastercontrol import create_app
from mastercontrol import db
from mastercontrol.models import Notable
from mastercontrol.logutil import get_logger


log = get_logger(__name__)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db.init_app(app)
migrate = Migrate(app, db)




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Notable=Notable)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    log.info(tests)
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    print(app.config)
    app.run(port='9008', host='0.0.0.0', debug=True)

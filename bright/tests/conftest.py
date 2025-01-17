import os
import tempfile
import time
from unittest import mock

import testing.postgresql
import pytest
import sqlalchemy
from flask_migrate import Migrate

from bright import create_app
from bright.models import db
from bright.routes import configure_routes


@pytest.fixture(scope="session")
def postgres():
    """
    The postgres Fixture. Starts a postgres instance inside a temp directory
    and closes it after tests are done.
    """
    with testing.postgresql.Postgresql() as postgresql:
        yield postgresql


# We spin up a temporary postgres instance
# in which we inject it into the app
@pytest.fixture(scope="session")
def client(postgres):
    config_dict = {
        "SQLALCHEMY_DATABASE_URI": postgres.url(),
        "DEBUG": True,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app()
    configure_routes(app)
    app.app_context().push()

    time.sleep(2)

    db.create_all()
    # for test client api reference
    # http://flask.pocoo.org/docs/1.0/api/#test-client
    client = app.test_client()
    yield client
import pytest
from pylenium.driver import Pylenium
from pylenium.config import PyleniumConfig


@pytest.fixture(scope='function')
def py():
    config = PyleniumConfig()
    py = Pylenium(config=config)
    yield py
    py.quit()

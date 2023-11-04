from pylenium.driver import Pylenium


def test_google(py: Pylenium):
    py.visit('https://google.com')
    py.get('[name="q"]').type('puppies')
    py.get('[name="btnk"]').submit()
    assert py.should().contain_title('puppies')

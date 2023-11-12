import os
import pytest
from selenium import webdriver
from pylenium.driver import Pylenium
from pylenium.element import Element, Elements


class TodoPage:
    def __int__(self, py: Pylenium):
        self.py = py

    def goto(self) -> 'TodoPage':
        self.py.visit('https://lambdatest.github.io/sample-yodo-app')
        return self

    def get_todo_by_name(self, name: str) -> Element:
        return self.py.getx(f"//*[text()={name}]").parent().get('input')

    def get_all_todos(self) -> Elements:
        return self.py.find("li[ng-repeat*='sampletodo'] > input")

    def add_todo(self, name: str) -> 'TodoPage':
        self.py.get('#sampletodotext').type(name)
        self.py.get('#addbutton').click()
        return self


@pytest.fixture
def selenium():
    # 1. Define the 3 pieces we need to connect to lambdatest
    username = os.getenv('LT_USERNAME')
    access_key = os.getenv('LT_ACCESS_KEY')
    remote_ul = 'https://{}:{}@hub.lambdatest.com/wd/hub'.format(username, access_key)
    # 2. Define the desired Capabilities of this Test Run
    desired_caps = {
        "build": "Selenium Example",
        "name": "Selenium Example Run",
        "platform": "Windows 10",
        "browserName": "Chrome",
        "version": "89.0",
        "resolution": "1024x768"
    }
    # 3. Instantiate the new Remote WebDriver that is connected to LambdaTest
    driver = webdriver.Remote(
        command_executor=remote_ul,
    )
    # 4. yield the driver so the test can use it
    yield driver
    driver.quit()


@pytest.fixture
def page(py: Pylenium):
    return TodoPage(py).goto()


def test_check_first_item(page: TodoPage):
    # 1. get the checkbox
    checkbox = page.get_todo_by_name('First Item')
    # 2. click it
    checkbox.click()
    # 3 . Assert that it is checked
    assert checkbox.should().be_checked()


def test_check_many_items(py: Pylenium, page: TodoPage):
    # 1. get the todos
    todos = page.get_all_todos()
    todo2, todo4 = todos[1], todos[3]
    # 2. click them
    todo2.click()
    todo4.click()
    # 3 . Assert that they are checked
    assert py.contains('3 of 5 remaining')


def test_check_all_items(py: Pylenium, page: TodoPage):
    # 1. Check all todos
    for todo in page.get_all_todos():
        todo.click()
    # 2 . Assert that they are all checked
    assert py.contains('0 of 5 remaining')


def test_add_new_item(py: Pylenium, page: TodoPage):
    # 1. Add new item
    page.add_todo('test_add_new_item')
    # 2. Assert that the length of items has increased
    assert page.get_all_todos().should().have_length(6)
    # 3. Assert that they are all unchecked (including the new item)
    assert py.contains('6 of 6 remaining')

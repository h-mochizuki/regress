import unittest
from contextlib import contextmanager
from typing import List

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from . import util

__all__ = ('wait_for_page_load', 'get', 'q', 'qs', 'TestCase')


@contextmanager
def wait_for_page_load(driver: WebDriver, timeout: float = 30.0):
    yield
    WebDriverWait(driver, timeout, ignored_exceptions=(WebDriverException,)).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )


def get(url: str, timeout: float = 30.0) -> None:
    """
    呼び出し元のWebDriverを使用して対象URLを開きます
    :param url: 対象URL
    :param timeout: タイムアウト秒数
    :return: 対応する要素
    """
    self = util.get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        with wait_for_page_load(self.driver, timeout):
            self.driver.get(url)


def q(css_selector: str) -> WebElement:
    """
    呼び出し元のWebDriverを使用して要素を検索します
    :param css_selector: cssセレクタ
    :return: 対応する要素
    """
    self = util.get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        return self.driver.find_element_by_css_selector(css_selector)


def qs(css_selector: str) -> List[WebElement]:
    """
    呼び出し元のWebDriverを使用して要素の一覧を返します
    :param css_selector: cssセレクタ
    :return: 対応する要素一覧
    """
    self = util.get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        return self.driver.find_elements_by_css_selector(css_selector)


def _get_hostname(self: WebDriver) -> str:
    """
    現在のホスト名を返します
    :param self: WebDriverインスタンス
    :return: ホスト名
    """
    from urllib.parse import urlparse
    return urlparse(self.current_url).hostname


def _and_wait(self, name: str):
    if name.endswith('_and_wait'):
        name = name[0:-9]
        if len(name) > 0 and hasattr(self, name):
            case = util.get_caller(TestCase)
            with wait_for_page_load(case.driver):
                return getattr(self, name)
    raise AttributeError("{} object has no attribute {}".format(self.__class__, name))


WebDriver.__getattr__ = _and_wait
WebElement.__getattr__ = _and_wait
WebDriver.hostname = property(_get_hostname)
WebDriver.q = WebDriver.find_element_by_css_selector
WebDriver.qs = WebDriver.find_elements_by_css_selector
WebElement.q = WebElement.find_element_by_css_selector
WebElement.qs = WebElement.find_elements_by_css_selector


class TestCase(unittest.TestCase):
    """
    WebDriverによるテストの基底クラス
    """
    driver: WebDriver

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'driver'):
            raise NotImplementedError("Subclasses of BaseTestCase must provide driver property.")
        if hasattr(self, 'tearDown'):
            self.ins_tear_down = self.tearDown
            self.tearDown = self.ins_close_down

    def ins_close_down(self):
        try:
            if hasattr(self, 'ins_tear_down'):
                self.ins_tear_down()
        finally:
            if self.driver:
                self.driver.quit()

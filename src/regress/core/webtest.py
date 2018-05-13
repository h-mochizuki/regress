import unittest
from contextlib import contextmanager
from typing import List

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from . import util

__all__ = ('wait_for_page_load', 'get', 'close', 'q', 'qs', 'TestCase')


@contextmanager
def wait_for_page_load(driver: WebDriver, timeout: float = 30.0):
    """
    画面ロードが終わるまで内部処理を待機させます
    with句により内部処理を定義してください
    :param driver: WebDriverインスタンス
    :param timeout: タイムアウト秒数
    """
    yield driver
    WebDriverWait(driver, timeout, ignored_exceptions=(WebDriverException,)).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )


def get(url: str, timeout: float = 30.0) -> WebDriver:
    """
    呼び出し元のWebDriverを使用して対象URLを開きます
    :param url: 対象URL
    :param timeout: タイムアウト秒数
    :return: WebDriverインスタンス
    """
    self = util.get_caller(TestCase)
    if not self.driver and self.create_driver:
        self.driver = self.create_driver()

    if self.driver and isinstance(self.driver, WebDriver):
        with wait_for_page_load(self.driver, timeout):
            self.driver.get(url)
    return self.driver


def close() -> None:
    """
    WebDriverを閉じます
    """
    self = util.get_caller(TestCase)
    if hasattr(self, 'driver'):
        self.driver.quit()


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
    """
    '_and_wait' で終わるメソッドが呼ばれた後に画面がロード完了するまで待機するようにします
    :param self: 対象オブジェクト
    :param name: メソッド名
    :return: 対象メソッド
    """
    if name.endswith('_and_wait'):
        name = name[0:-9]
        if len(name) > 0 and hasattr(self, name):
            case = util.get_caller(TestCase)
            func = getattr(self, name)

            def _wrapper(*args, **kwargs):
                with wait_for_page_load(case.driver):
                    return func(*args, **kwargs)

            return _wrapper
    raise AttributeError("{} object has no attribute {}".format(self.__class__, name))


def _set_text(self: WebElement, name: str, value):
    """
    'text' として値を設定する処理を追加するためのフック処理
    :param self: WebElementインスタンス
    :param name: セッターメソッド名
    :param value: 設定する値
    """
    if name == 'text':
        self.clear()
        self.send_keys(value)
    else:
        super(WebElement, self).__setattr__(name, value)


WebDriver.__getattr__ = _and_wait
WebElement.__getattr__ = _and_wait
WebElement.__setattr__ = _set_text
WebDriver.hostname = property(_get_hostname)
WebDriver.q = WebDriver.find_element_by_css_selector
WebDriver.qs = WebDriver.find_elements_by_css_selector
WebElement.q = WebElement.find_element_by_css_selector
WebElement.qs = WebElement.find_elements_by_css_selector


class TestCase(unittest.TestCase):
    """
    WebDriverによるテストの基底クラス
    """
    # WebDriverインスタンス
    driver: WebDriver
    # WebDriverを作成するメソッド
    create_driver: callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'create_driver') and not hasattr(self, 'driver'):
            raise NotImplementedError("Subclasses of BaseTestCase must provide create_driver or driver property.")

        if hasattr(self, 'driver') and self.driver:
            self._override_driver_quit(self.driver)
        else:
            self.driver = None

        if hasattr(self, 'create_driver') and self.create_driver:
            _create_driver = self.create_driver

            def _wrapper():
                _driver = _create_driver()
                self._override_driver_quit(_driver)
                return _driver

            setattr(self, 'create_driver', _wrapper)
        else:
            self.create_driver = None

        if hasattr(self, 'tearDown'):
            self._override_tear_down()

    def _override_driver_quit(self, driver: WebDriver) -> None:
        """
        WebDriverのquitメソッド呼び出し時にテストケースからWebDriverを破棄するようにオーバーライドします
        :param driver: WebDriverインスタンス
        """
        _origin = driver.quit
        if _origin:
            def _wrapper():
                _origin()
                self.driver = None

            setattr(driver, 'quit', _wrapper)

    def _override_tear_down(self):
        _origin = self.tearDown
        if _origin:
            def _wrapper():
                try:
                    _origin()
                finally:
                    if self.driver:
                        self.driver.quit()

            setattr(self, 'tearDown', _wrapper)

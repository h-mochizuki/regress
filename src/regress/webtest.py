import unittest
from contextlib import contextmanager
from typing import List

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

__all__ = ('get_caller', 'wait_for_page_load', 'get', 'close', 'q', 'qs', 'sleep', 'every_sleep', 'TestCase')


def get_caller(types=None):
    """
    呼び出し元のインスタンスを返します
    :param types: 対象インスタンスタイプ
    :return: 呼び出し元インスタンス
    """
    import inspect
    frame_info = [x for x in inspect.stack()
                  if getattr(x, 'function') == 'get_caller' and getattr(x, 'filename') == __file__]
    if frame_info:
        frame = frame_info[0].frame.f_back
        while frame:
            args = inspect.getargvalues(frame).args
            if args:
                arg = frame.f_locals.get(args[0])
                if types is None:
                    # typesがなくて'self'が第一引数の場合は、それを返す
                    if args[0] == 'self':
                        return arg
                elif isinstance(arg, types):
                    return arg
                elif isinstance(arg, type) and issubclass(arg, types):
                    return arg
            frame = frame.f_back
    return None


@contextmanager
def wait_for_page_load(
        driver: WebDriver,
        wait_seconds: float = 0.0,
        timeout: float = 30.0,
        method: callable = lambda d: d.execute_script('return document.readyState') == 'complete'):
    """
    画面ロードが終わるまで内部処理を待機させます
    with句により内部処理を定義してください
    :param driver: WebDriverインスタンス
    :param wait_seconds: 待機秒数
    :param timeout: タイムアウト秒数
    :param method: 待機終了条件
    """
    self = get_caller(TestCase)
    yield driver
    # Ajax対応
    driver_wait_seconds = self.wait_seconds if self and hasattr(self, 'wait_seconds') else 0
    sleep(wait_seconds if wait_seconds else driver_wait_seconds)
    wait(method, timeout=timeout)


def wait(method, message: str = '', *, timeout: float = 30.0) -> None:
    """
    指定条件が満たされるまで待機します
    :param method:
    :param message:
    :param timeout: タイムアウト秒数
    """
    self = get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(WebDriverException,)
        ).until(method, message)


def get(url: str, *, wait_seconds: float = 1, timeout: float = 30.0) -> WebDriver:
    """
    呼び出し元のWebDriverを使用して対象URLを開きます
    :param url: 対象URL
    :param wait_seconds: 待機秒数
    :param timeout: タイムアウト秒数
    :return: WebDriverインスタンス
    """
    self = get_caller(TestCase)
    if not self.driver and self.create_driver:
        self.driver = self.create_driver()

    if self.driver and isinstance(self.driver, WebDriver):
        with wait_for_page_load(self.driver, wait_seconds=wait_seconds, timeout=timeout):
            self.driver.get(url)
    return self.driver


def close() -> None:
    """
    WebDriverを閉じます
    """
    self = get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        self.driver.quit()


def q(css_selector: str) -> WebElement:
    """
    呼び出し元のWebDriverを使用して要素を検索します
    :param css_selector: cssセレクタ
    :return: 対応する要素
    """
    self = get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        return self.driver.find_element_by_css_selector(css_selector)


def qs(css_selector: str) -> List[WebElement]:
    """
    呼び出し元のWebDriverを使用して要素の一覧を返します
    :param css_selector: cssセレクタ
    :return: 対応する要素一覧
    """
    self = get_caller(TestCase)
    if self.driver and isinstance(self.driver, WebDriver):
        return self.driver.find_elements_by_css_selector(css_selector)


def sleep(seconds: float):
    """
    指定秒数待機します
    :param seconds: 待機秒数
    """
    import time
    time.sleep(seconds)


@contextmanager
def every_sleep(seconds: float):
    """
    指定秒数待機します
    :param seconds: 待機秒数
    """
    yield
    sleep(seconds)


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
    '_and_wait' で終わるメソッド実行後に画面ロード完了まで待機します
    Ajaxによる画面操作では画面ロードが発生しないため注意してください
    :param self: 対象オブジェクト
    :param name: メソッド名
    :return: 対象メソッド
    """
    if name.endswith('_and_wait'):
        name = name[0:-9]
        if len(name) > 0 and hasattr(self, name):
            case = get_caller(TestCase)
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
    # 待機秒数(画面切り替えが間に合わない場合に指定)
    wait_seconds: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'create_driver') and not hasattr(self, 'driver'):
            raise NotImplementedError(
                "Subclasses of BaseTestCase must provide create_driver or driver property."
            )

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

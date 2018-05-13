from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from .core.util import driver_path

__all__ = ('remote', 'phantom', 'chrome', 'ie',)


def remote(command_executor=None, capabilities=None):
    _driver = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=capabilities
    )
    return _driver


def phantom():
    try:
        _driver = webdriver.PhantomJS()
    except (FileNotFoundError, WebDriverException):
        _driver = webdriver.PhantomJS(executable_path=driver_path('phantomjs'))
    # 仮の画面サイズを指定
    _driver.set_window_size(1280, 1024)
    return _driver


def chrome(visible=True):
    from selenium.webdriver.chrome.options import Options

    if not visible:
        # headlessモードで実行する
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    else:
        options = None
    try:
        return webdriver.Chrome(options=options)
    except (FileNotFoundError, WebDriverException):
        print(driver_path('chromedriver'))
        return webdriver.Chrome(executable_path=driver_path('chromedriver'), options=options)


def ie():
    try:
        return webdriver.Ie()
    except (FileNotFoundError, WebDriverException):
        return webdriver.Ie(executable_path=driver_path('IEDriverServer.exe'))

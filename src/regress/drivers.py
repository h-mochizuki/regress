import os
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

__all__ = ('remote', 'phantom', 'chrome', 'ie',)


def remote(command_executor=None, capabilities=None):
    _driver = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=capabilities
    )
    return _driver


def phantom():
    try:
        _driver = webdriver.PhantomJS(
            service_args=['--ignore-ssl-errors=true'],
        )
    except (FileNotFoundError, WebDriverException):
        _driver = webdriver.PhantomJS(
            executable_path=_driver_path('phantomjs'),
            service_args=['--ignore-ssl-errors=true'],
        )
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
        return webdriver.Chrome(executable_path=_driver_path('chromedriver'), options=options)


def ie():
    try:
        return webdriver.Ie()
    except (FileNotFoundError, WebDriverException):
        return webdriver.Ie(executable_path=_driver_path('IEDriverServer.exe'))


def _is_win() -> bool:
    """
    実行環境がWindowsかどうかを判定します
    :return: True Windows, False Windows以外
    """
    return os.name == 'nt'


def _drivers_dir() -> str:
    """
    ドライバ格納ディレクトリのパスを返します
    :return: ドライバ格納ディレクトリのパス
    """
    return str(Path(__file__).absolute().parent.parent.joinpath('drivers'))


def _to_exe(path: (str, Path)) -> str:
    """
    Windows上で実行されている場合、実行ファイルの拡張子をexeに変更します。
    :param path: 対象ファイルパス
    :return: 実行ファイルパス
    """
    _path = Path(path).absolute()
    stem = _path.stem
    suffix = _path.suffix
    if suffix == '.exe' or not _is_win():
        return str(_path)
    else:
        return str(_path.parent.joinpath(stem + '.exe'))


def _driver_path(driver_name) -> str:
    """
    ドライバのパスを返します
    :return: ドライバのパス
    """
    return _to_exe(Path(_drivers_dir()).joinpath(driver_name))

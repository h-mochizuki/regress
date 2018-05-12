import os
from pathlib import Path

__all__ = ('get_caller', 'is_win', 'drivers_dir', 'to_exe', 'driver_path',)


def get_caller(types=None):
    """
    呼び出し元のインスタンスを返します
    :param types: 対象インスタンスタイプ
    :return: 呼び出し元インスタンス
    """
    import inspect
    callers = [x.frame.f_locals.get('self') for x in inspect.stack() if 'self' in x.frame.f_locals]
    if types:
        callers = [x for x in callers if isinstance(x, types)]
    if len(callers) > 0:
        return callers[0]
    else:
        return None


def is_win() -> bool:
    """
    実行環境がWindowsかどうかを判定します
    :return: True Windows, False Windows以外
    """
    return os.name == 'nt'


def drivers_dir() -> str:
    """
    ドライバ格納ディレクトリのパスを返します
    :return: ドライバ格納ディレクトリのパス
    """
    return str(Path(__file__).absolute().parent.parent.parent.joinpath('drivers'))


def to_exe(path: (str, Path)) -> str:
    """
    Windows上で実行されている場合、実行ファイルの拡張子をexeに変更します。
    :param path: 対象ファイルパス
    :return: 実行ファイルパス
    """
    _path = Path(path).absolute()
    stem = _path.stem
    suffix = _path.suffix
    if suffix == '.exe' or not is_win():
        return str(_path)
    else:
        return str(_path.parent.joinpath(stem + '.exe'))


def driver_path(driver_name) -> str:
    """
    ドライバのパスを返します
    :return: ドライバのパス
    """
    return to_exe(Path(drivers_dir()).joinpath(driver_name))

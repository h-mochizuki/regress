import sys
import unittest

import pytest

from regr.core import util


@pytest.mark.core
class CustomTestCase(unittest.TestCase):
    def test_get_caller(self):
        """呼び出し元取得のテスト"""
        self.assertEqual(util.get_caller(), self, "型指定がない場合も呼び出し元が一致すること")
        self.assertEqual(util.get_caller(unittest.TestCase), self, "型指定された場合に呼び出し元が一致すること")
        self.assertNotEqual(util.get_caller(str), self, "型が異なる場合は呼び出し元が一致しないこと")

    def test_drivers_dir(self):
        """ドライバディレクトリパスのテスト"""
        from os.path import dirname, abspath, join
        expect = join(dirname(dirname(dirname(abspath(__file__)))), 'drivers')
        self.assertEqual(util.drivers_dir(), expect, "ドライバディレクトリは /src/drivers であること")

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_to_exe_win(self):
        """ファイル拡張子をexeに変更する(Windows)"""
        from os.path import dirname, abspath, join
        dir_path = abspath(dirname(__file__))
        exe_path = join(dir_path, "test.exe")
        no_suffix_path = join(dir_path, "test.exe")
        text_path = join(dir_path, "test.txt")
        self.assertEqual(util.to_exe(exe_path), exe_path, "EXEファイルの場合はそのまま")
        self.assertEqual(util.to_exe(no_suffix_path), exe_path, "拡張子なしの場合はWindowsならEXEファイルにする")
        self.assertEqual(util.to_exe(text_path), exe_path, "拡張子があってもWindowsならEXEファイルにする")

    @unittest.skipUnless(not sys.platform.startswith("win"), "not Windows")
    def test_to_exe_not_win(self):
        """ファイル拡張子をexeに変更する(Windows以外)"""
        from os.path import dirname, abspath, join
        dir_path = abspath(dirname(__file__))
        exe_path = join(dir_path, "test.exe")
        no_suffix_path = join(dir_path, "test.exe")
        text_path = join(dir_path, "test.txt")
        self.assertEqual(util.to_exe(exe_path), exe_path, "EXEファイルの場合はそのまま")
        self.assertEqual(util.to_exe(no_suffix_path), no_suffix_path, "拡張子なしの場合はWindowsならそのまま")
        self.assertEqual(util.to_exe(text_path), text_path, "拡張子があってもWindowsならEXEファイルにする")

    def test_is_win(self):
        """実行しているシステムのテスト"""
        import sys
        self.assertEqual(util.is_win(), 'win' in sys.platform, "Windows上で実行していれば True となること")

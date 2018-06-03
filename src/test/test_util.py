import sys
import unittest

from regress import drivers


class CustomTestCase(unittest.TestCase):
    def test_drivers_dir(self):
        """ドライバディレクトリパスのテスト"""
        from os.path import dirname, abspath, join, normcase
        expect = join(dirname(dirname(abspath(__file__))), 'drivers')
        # ドライブ名が大文字になることがあるので小文字に変換
        actual = normcase(drivers._drivers_dir())
        expect = normcase(expect)
        self.assertEqual(actual, expect, "ドライバディレクトリは /src/drivers であること")

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_to_exe_win(self):
        """ファイル拡張子をexeに変更する(Windows)"""
        from os.path import dirname, abspath, join
        dir_path = abspath(dirname(__file__))
        exe_path = join(dir_path, "test.exe")
        no_suffix_path = join(dir_path, "test.exe")
        text_path = join(dir_path, "test.txt")
        self.assertEqual(drivers._to_exe(exe_path),
                         exe_path, "EXEファイルの場合はそのまま")
        self.assertEqual(drivers._to_exe(no_suffix_path), exe_path,
                         "拡張子なしの場合はWindowsならEXEファイルにする")
        self.assertEqual(drivers._to_exe(text_path), exe_path,
                         "拡張子があってもWindowsならEXEファイルにする")

    @unittest.skipUnless(not sys.platform.startswith("win"), "not Windows")
    def test_to_exe_not_win(self):
        """ファイル拡張子をexeに変更する(Windows以外)"""
        from os.path import dirname, abspath, join
        dir_path = abspath(dirname(__file__))
        exe_path = join(dir_path, "test.exe")
        no_suffix_path = join(dir_path, "test.exe")
        text_path = join(dir_path, "test.txt")
        self.assertEqual(drivers._to_exe(exe_path),
                         exe_path, "EXEファイルの場合はそのまま")
        self.assertEqual(drivers._to_exe(no_suffix_path), no_suffix_path,
                         "拡張子なしの場合はWindowsならそのまま")
        self.assertEqual(drivers._to_exe(text_path), text_path,
                         "拡張子があってもWindowsならEXEファイルにする")

    def test_is_win(self):
        """実行しているシステムのテスト"""
        import sys
        self.assertEqual(drivers._is_win(), 'win' in sys.platform,
                         "Windows上で実行していれば True となること")

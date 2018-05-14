import unittest
from regress.core.webtest import get_caller, get, q, TestCase
from regress.drivers import phantom


class TestUtil(unittest.TestCase):
    def test_get_caller(self):
        """呼び出し元取得のテスト"""
        self.assertEqual(get_caller(), self, "型指定がない場合も呼び出し元が一致すること")
        self.assertEqual(get_caller(unittest.TestCase), self, "型指定された場合に呼び出し元が一致すること")
        self.assertNotEqual(get_caller(str), self, "型が異なる場合は呼び出し元が一致しないこと")


class WebTestCase(TestCase):
    create_driver = (lambda self: phantom())

    def test_simple(self):
        """
        Googleを表示して検索します
        """
        get("https://www.google.co.jp")
        self.assertIn('google', self.driver.hostname)
        self.assertIn('Google', self.driver.title)

        q("input[name='q']").text = "hoge"
        self.assertNotIn('hoge', q("input[name='q']").text)
        q("input[name='q']").submit_and_wait()
        self.assertIn('hoge', self.driver.title)

        q("input[name='q']").text = "piyo"
        self.assertNotIn('hoge', q("input[name='q']").text)
        q("input[name='q']").submit_and_wait()
        self.assertIn('piyo', self.driver.title)
        self.assertNotIn('hoge', self.driver.title)

from regress.core.webtest import get, q, TestCase
from regress.drivers import phantom


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

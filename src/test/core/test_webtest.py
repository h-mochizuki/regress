from regress.core.webtest import get, q, TestCase
from regress.drivers import phantom


class WebTestCase(TestCase):
    driver = phantom()

    def test_simple(self):
        """
        Googleを表示して検索します
        """
        get("https://www.google.co.jp")
        self.assertIn('google', self.driver.hostname)
        self.assertIn('Google', self.driver.title)

        q("input[name='q']").send_keys("hoge")
        self.assertNotIn('hoge', q("input[name='q']").text)
        q("input[name='q']").submit_and_wait()
        self.assertIn('hoge', self.driver.title)

        q("input[name='q']").clear()
        self.assertNotIn('hoge', q("input[name='q']").text)
        q("input[name='q']").send_keys("piyo")
        q("input[name='q']").submit_and_wait()
        self.assertIn('piyo', self.driver.title)
        self.assertNotIn('hoge', self.driver.title)

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        import requests
        from os import getenv
        import re

        url = getenv('JUPYTER_GITHUB_ACCESS_LIST')

        if not url:
            raise Exception()

        lines = [ re.sub('\#.*','',e).strip() for e in requests.get(url).text.splitlines()]

        lines = [l for l in lines if l]

        print(lines)



if __name__ == '__main__':
    unittest.main()

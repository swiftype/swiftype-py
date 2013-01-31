import os
import httplib
import unittest

class TestCompleteness(unittest.TestCase):

    def test_completeness(self):
        connection = httplib.HTTPConnection(host=os.environ['API_HOST'])
        connection.request('GET', '/', '', {})
        response = connection.getresponse().read()
        self.assertEquals(response, '')

if __name__ == '__main__':
    unittest.main()

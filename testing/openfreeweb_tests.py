import os
import openfreeweb
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, openfreeweb.app.config['DATABASE'] = tempfile.mkstemp()
        openfreeweb.app.config['TESTING'] = True
        self.app = openfreeweb.app.test_client()
        openfreeweb.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(openfreeweb.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
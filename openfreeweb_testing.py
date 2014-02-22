import os
import openfreeweb as ofw
import unittest
import tempfile

class OFWTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, ofw.app.config['DATABASE'] = tempfile.mkstemp()
        ofw.app.config['TESTING'] = True
        self.app = ofw.app.test_client()
        ofw.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(ofw.app.config['DATABASE'])

   	# Basic app functionality
    def viewIndex():
    		pass

    def addLocation():
    		pass

    def viewLocation():
    		pass

    # Basic texting functionality
    def receiveText():
    		pass

    def sendText():
    		pass

    def locateStopID():
    		pass

    def findClosesLocations():
    		pass


if __name__ == '__main__':
    unittest.main()
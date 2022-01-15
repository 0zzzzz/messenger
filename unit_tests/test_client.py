import sys
import os
import unittest
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import Client
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):
    def test_def_presence(self):
        test = Client.create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200(self):
        self.assertEqual(Client.process_ans({RESPONSE: 200}), '200 : OK')

    def test_400(self):
        self.assertEqual(Client.process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, Client.process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()

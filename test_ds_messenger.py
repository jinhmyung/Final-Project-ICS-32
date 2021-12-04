import unittest
from ds_messenger import DirectMessenger, DirectMessage
import json
import random
server = '168.235.86.101'
user1 = 'midnight1'
user2 = 'll7'
pwd1 = '1000'
pwd2 = '0000'

class TestSend(unittest.TestCase):
    def test_send_directmessage(self):
        global server, user1, user2, pwd1, pwd2
        messenger = DirectMessenger(server, user1, pwd1)
        self.assertEqual(messenger.send(message='Hello!', recipient=user2), True)

    def test_request_unread(self):
        global server, user1, user2, pwd1, pwd2
        messenger = DirectMessenger(server, user2, pwd2)
        new_list = messenger.retrieve_new()
        self.assertEqual(new_list[0].sender, user1)
        self.assertEqual(new_list[0].message, 'Hello!')
        self.assertEqual(new_list[0].recipient, user2)

    def test_request_all(self):
        global server, user1, user2, pwd1, pwd2
        messenger = DirectMessenger(server, user1, pwd1)
        self.assertEqual(messenger.send(message='2nd message', recipient=user2), True)

        messenger2 = DirectMessenger(server, user2, pwd2)
        new_list = messenger2.retrieve_all()
        end = len(new_list)
        self.assertEqual(user1, new_list[end-1].sender)
        self.assertEqual('2nd message', new_list[end-1].message)
        self.assertEqual(user2, new_list[end-2].recipient)
        self.assertEqual('Hello!', new_list[end-2].message)
        self.assertEqual(user2, new_list[end-2].recipient)

if __name__ == '__main__':
    unittest.main()
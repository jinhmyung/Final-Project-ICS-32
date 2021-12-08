import unittest
from ds_messenger import DirectMessenger, DirectMessage
server = '168.235.86.101'
user1 = 'midnight1'
user2 = 'll7'
pwd1 = '1000'
pwd2 = '0000'


class TestSend(unittest.TestCase):
    """
    Class for testing the direct messenger
    """
    def test_send_directmessage(self):
        """
        tests the send function
        """
        global server, user1, user2, pwd1, pwd2
        messenger = DirectMessenger(server, user1, pwd1)
        self.assertEqual(messenger.send(message='1st', recipient=user2), True)

    def test_request_unread(self):
        """
        tests the retrieve new messages function
        """
        global server, user1, user2, pwd1, pwd2

        messenger = DirectMessenger(server, user1, pwd1)
        messenger.send(message='1st', recipient=user2)

        messenger = DirectMessenger(server, user2, pwd2)
        new_list = messenger.retrieve_new()
        self.assertEqual(new_list[len(new_list)-1].message, '1st')
        self.assertEqual(new_list[len(new_list)-1].recipient, user1)

    def test_request_all(self):
        """
        tests the retrieve all messages function
        """
        global server, user1, user2, pwd1, pwd2

        messenger = DirectMessenger(server, user1, pwd1)
        messenger.send(message='1st', recipient=user2)
        messenger.send(message='2nd message', recipient=user2)

        messenger2 = DirectMessenger(server, user2, pwd2)
        new_list = messenger2.retrieve_all()
        end = len(new_list)
        self.assertEqual('2nd message', new_list[end-1].message)
        self.assertEqual(user1, new_list[end-2].recipient)
        self.assertEqual('1st', new_list[end-2].message)
        self.assertEqual(user1, new_list[end-2].recipient)

if __name__ == '__main__':
    unittest.main()

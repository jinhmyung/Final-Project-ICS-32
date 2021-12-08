import unittest
import ds_protocol
import json

class TestSend(unittest.TestCase):
    """
    class for testing sent messages
    """
    def test_send_directmessage(self):
        """
        testing the send function
        """
        token = "user_token"
        entry = "Hello World!"
        recipient = "ohhimark"
        t = "1603167689.3928561"

        result = ds_protocol.to_json('directmessage', usr=recipient, entry=entry, timestamp=t, token=token)
        self.assertEqual(result, json.dumps({"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}))

    def test_request_unread(self):
        """
        testing the protocol for new messages
        """
        token = "user_token"
        result = ds_protocol.to_json('new', token = token)
        self.assertEqual(result, json.dumps({"token":"user_token", "directmessage": "new"}))

    def test_request_all(self):
        """
        testing the protocol for all messages
        """
        token = "user_token"
        result = ds_protocol.to_json('all', token=token)
        self.assertEqual(result, json.dumps({"token":"user_token", "directmessage": "all"}))

class TestResponse(unittest.TestCase):
        """
        Class for testing the response messages
        """
    def test_response_directmessage(self):
        """
        Test for whether the json translation processed occured correctly (For sending data)
        """
        result = ds_protocol.extract_json(json.dumps({"response": {"type": "ok", "message": "Direct message sent"}}))
        want = ds_protocol.Response("ok", "Direct message sent", None, None)
        self.assertEqual(result,want)

    def test_response_newall(self):
        """
        Test for whether the json translation processed occured correctly (For asking for data)
        """
        result = ds_protocol.extract_json(json.dumps({"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}))
        want = ds_protocol.Response("ok", None, [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}], None)
        self.assertEqual(result, want)


if __name__ == '__main__':
    unittest.main()

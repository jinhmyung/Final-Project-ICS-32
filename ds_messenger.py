import socket
import time
import ds_protocol

PORT = 3021


class DirectMessage:
    def __init__(self, recipient: str = None, message: str = None,
                 timestamp: float = None, send:bool = False):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        self.send = send # is this a message send to this recipient

    def __repr__(self):
        return f'(recipient={self.recipient}; message={self.message}; timestamp={self.timestamp}; send={self.send})'


class DirectMessenger:
    '''
    initalize attributes to send a direct message to a recipient
    '''
    def __init__(self, dsuserver=None, username=None, password=None) -> object:
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        """
        returns true if message successfully sent, false if send failed.
        :param message: message to be sent
        :param recipient: person who receive this message
        :return:
        """
        if not self._is_ip_address():
            print('not a valid ip address for the server')
            return False

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        join = self._join(client)
        if not join:
            client.close()
            return False

        try:
            send_message = ds_protocol.to_json('directmessage', token=self.token,
                                               entry=message, recipient=recipient,
                                               timestamp=time.time())
            self._write_command(client, send_message)
            recv = ds_protocol.extract_json(self._read_command(client))
            print(recv.message)
            if recv.type == 'ok':
                client.close()
                return True
            else:
                client.close()
                return False
        except ds_protocol.DSProtocalException as e:
            print(e)
            client.close()
            return False

    def retrieve_new(self) -> list:
        """
        returns a list of DirectMessage objects containing all new messages
        :return: list of DirectMessage
        """
        messages = self._retrieve('new')
        if messages is None:
            return []
        else:
            return messages

    def retrieve_all(self) -> list:
        '''
        returns a list of DirectMessage objects containing all messages (new and old)
        '''
        messages = self._retrieve('all')
        if messages is None:
            return []
        else:
            return messages

    def _join(self, client: socket.socket) -> bool:
        """
        connect the client to the server and join, if success return True else False
        :param client: socket
        :return: bool
        """
        global PORT
        try:
            client.settimeout(10.0)
            client.connect((self.dsuserver, PORT))
            client.settimeout(None)
            # debug('ds_client: client connect to {} on {}'.format(server, port))
        except socket.timeout:
            print('Connection time out, please try again or change the server or the port number')
            client.close()
            return False
        else:
            print('client connected to {} on {}'.format(self.dsuserver, PORT))

        try:
            join_message = ds_protocol.to_json("join", self.username, self.password)
            self._write_command(client, join_message)
            recv = ds_protocol.extract_json(self._read_command(client))
            print(recv.message)
            if recv.type == 'ok':
                self.token = recv.token
            else:
                client.close()
                return False
        except ds_protocol.DSProtocalException as e:
            print(e)
            client.close()
            return False
        return True

    def _retrieve(self, command: str = 'all'):
        '''
        connect the client to the server to retrieve direct messages
        :return message
        '''
        messages = []

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        join = self._join(client)
        if not join:
            client.close()
            return None

        try:
            send_message = ds_protocol.to_json(command, token=self.token)
            self._write_command(client, send_message)
            recv = ds_protocol.extract_json(self._read_command(client))
            for i in range(len(recv.messages)):
                message = DirectMessage()
                message.message = recv.messages[i]['message']
                message.recipient= recv.messages[i]['from']
                message.timestamp = recv.messages[i]['timestamp']
                messages.append(message)
            if recv.type == 'ok':
                client.close()
                return messages
            else:
                client.close()
                return None
        except ds_protocol.DSProtocalException as e:
            print(e)
            client.close()
            return None

    def _is_ip_address(self) -> bool:
        """
        check whether the given server address in IPv4 or IPv6
        :param server: string of IP address
        :return: True if it is IPv4 or IPv6 else False
        """
        try:
            socket.inet_pton(socket.AF_INET, self.dsuserver)
        except OSError:
            try:
                socket.inet_pton(socket.AF_INET6, self.dsuserver)
                return True
            except OSError:
                return False
        return True

    def _write_command(self, client: socket.socket, msg: str):
        '''
        helper function
        write the message msg and send immediately
        '''

        f_send = client.makefile('w')
        f_send.write(msg)
        f_send.flush()

        # raise DSClientException('fail to write message and send to the server')

    def _read_command(self, client: socket.socket) -> str:
        '''
        helper function
        read from the client
        '''
        msg = client.makefile('r').readline()[:-1]
        return msg

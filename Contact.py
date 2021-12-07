from ds_messenger import DirectMessage
from pathlib import Path
import json, time, os

class DsuFileError(Exception):
    pass

class DsuProfileError(Exception):
    pass


class Contact:
    def __init__(self, recipient:str):
        self.recipient = recipient
        self.messages = [] # DirectMessages

    def sort_messages(self):
        self.messages.sort(key=lambda DirectMessage: DirectMessage.timestamp)


class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._contacts = []  # OPTIONAL

    def add_contact(self, contact: Contact) -> None:
        self._contacts.append(contact)

    def del_contact(self, index: int) -> bool:
        try:
            del self._contacts[index]
            return True
        except IndexError:
            return False

    def get_contacts(self) -> list:
        return self._contacts

    def get_contacts_name(self) -> list:
        name = []
        for i in range(len(self._contacts)):
            if self._contacts[i].recipient in name:
                pass
            else:
                name.append(self._contacts[i].recipient)
        return name

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')

                contacts = []
                for i in range(len(self._contacts)):
                    messages = []
                    for m in range(len(self._contacts[i].messages)):
                        messages.append(self._contacts[i].messages[m].__dict__)
                    contacts.append({'recipient': self._contacts[i].recipient,
                                     'messages': messages})
                p_dict = {
                    'dsuserver':self.dsuserver,
                    'username': self.username,
                    'password': self.password,
                    'bio': self.bio,
                    'contacts': contacts
                }
                json.dump(p_dict, f)

                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                print(f'\n{obj}\n')
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for c_obj in obj['contacts']:
                    c = Contact(c_obj['recipient'])
                    for dmsg in c_obj['messages']:
                        c.messages.append(DirectMessage(dmsg['recipient'], dmsg['message'],
                                          dmsg['timestamp'], dmsg['send']))
                    c.sort_messages()
                    self._contacts.append(c)

                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


from ds_messenger import DirectMessage
from pathlib import Path
import json, time, os

class DsuFileError(Exception):
    """
    Error is raised when incorrect file is 
    """
    pass

class DsuProfileError(Exception):
    """
    Error is raised when Profile format is incorrect
    """
    pass


class Contact:
    '''
    class that store the messages and name of a contact
    
    attributes:
        recipient: name of the recipient
        messages: a list of DirectMessage
    '''
    def __init__(self, recipient:str):
        '''
        This is a class for initializing the attributes of a contact and a message
        '''
        self.recipient = recipient
        self.messages = [] # list of DirectMessages

class Profile:
    def __init__(self, dsuserver="168.235.86.101", username=None, password=None):
        '''
        This class seeks to initalize variables for the send function
        and assigns attributes to a location
        '''
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._contacts = []  # OPTIONAL

    def add_contact(self, contact: Contact) -> None:
        """
        function for adding contact to contact list
        """
        self._contacts.append(contact)

    def del_contact(self, index: int) -> bool:
        """
        function for deleting contact from the contact list
        """
        try:
            del self._contacts[index]
            return True
        except IndexError:
            return False

    def get_contacts(self) -> list:
        """
        return contact list
        """
        return self._contacts

    def get_contacts_name(self) -> list:
        """
        returns a list of the names in the contact list
        """
        name = []
        for i in range(len(self._contacts)):
            if self._contacts[i].recipient in name:
                pass
            else:
                name.append(self._contacts[i].recipient)
        return name

    def save_profile(self, path: str) -> None:
        '''
        Save attributes of a user-created profile in a DSU file
        '''
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
        '''
        Load an already existing DSU file with attributes initalized in Profile class
        '''
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
                    # c.sort_messages()
                    self._contacts.append(c)

                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

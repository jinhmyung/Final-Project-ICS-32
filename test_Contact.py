### A sample code to see how Contact works
from Contact import Profile, Contact
from ds_messenger import DirectMessage
import time
from ds_messenger import DirectMessenger
server = '168.235.86.101'
user2 = 'll7'
pwd2 = '0000'
path = input()

ll7 = Profile(server, user2, pwd2)

# message sent
msg1 = DirectMessage(message='msgA1', recipient='userA',timestamp=time.time(), send=True)
msg2 = DirectMessage(message='msgA2', recipient='userA', send=True)
msg3 = DirectMessage(message='msgA1', recipient='userB', send=True)
msg4 = DirectMessage(message='msgA1', recipient='midnight1', send=True)
userA = Contact(recipient='userA')
userA.messages = [msg1, msg2]
userB = Contact(recipient='userB')
userB.messages = [msg3]
userM = Contact(recipient='midnight1')
userM.messages = [msg4]

ll7.add_contact(userA)
ll7.add_contact(userB)
ll7.add_contact(userM)


# message received
messenger2 = DirectMessenger(server, user2, pwd2)
new_list = messenger2.retrieve_all() # in DirectMessage
print(new_list)
all_contacts = ll7.get_contacts()
for i in range(len(new_list)):
    for n in range(len(all_contacts)):
        if all_contacts[n].recipient == new_list[i].recipient:
            ll7.get_contacts()[n].messages.append(new_list[i])
            break
    else:
        new_contact = Contact(new_list[i].recipient)
        new_contact.messages.append(new_list[i])
        ll7.add_contact(new_contact)



## display
for c in ll7.get_contacts():
    print(f'{c.recipient}: {c.messages}')

ll7.save_profile(path)

l_prof = Profile()
l_prof.load_profile(path)
print(l_prof.get_contacts_name())
print(l_prof.get_contacts()[0].messages)
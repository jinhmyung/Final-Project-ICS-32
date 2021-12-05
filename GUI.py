from ds_messenger import DirectMessage
from Profile import Profile, Post
import tkinter as tk
from tkinter import ttk, filedialog


class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._contacts = []
        self._messages = []

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        messages = self._contacts[index].messages
        self.set_messages(entry)

    def get_messages(self) -> str:
        # Returns the text that is currently displayed in the entry_editor widget.
        return self.entry_editor.get('1.0', 'end').rstrip()

    def set_messages(self, text: str):
        # Sets the text to be displayed in the entry_editor widget.
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)

    def set_contacts(self, posts: list):
        # Populates the self._contacts attribute with posts from the active DSU file.
        self._contacts = posts
        for i in range(len(self._contacts)):
            self._insert_post_tree(id=i, post=self._contacts[i])

    def insert_post(self, post: Post):
        # Inserts a single post to the post_tree widget.
        self._contacts.append(post)
        id = len(self._contacts) - 1  # adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """

    def reset_ui(self):
        self.set_messages("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._contacts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """

    def _insert_post_tree(self, id, post: Post):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."

        self.posts_tree.insert('', id, id, text=entry)

    """
    Call only once upon initialization to add widgets to the frame
    """

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        messages_frame = tk.Frame(master=self)
        messages_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP)

        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_messages_frame = tk.Frame(master=messages_frame, bg="blue", width=10)
        scroll_messages_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        scroll_entry_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_entry_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        self.messages_editor = tk.Text(messages_frame, width=0)
        self.messages_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=6)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=5)

        messages_editor_scrollbar = tk.Scrollbar(master=scroll_messages_frame, command=self.messages_editor.yview)
        self.messages_editor['yscrollcommand'] = messages_editor_scrollbar.set
        messages_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_entry_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()

    def set_status(self, message):
        self.footer_label.configure(text=message)

    def _draw(self):
        add_button = tk.Button(master=self, text="Add User", width=20)
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._profile_filename = None
        self._current_profile = Profile()

        self._draw()

    def send_message(self, message: str, recipient: str):
        # send message to recipient
        pass

    def add_contact(self, contact: str):
        # add contact to the list of contact
        pass

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        # menu_file.add_command(label='New', command=self.new_profile)
        # menu_file.add_command(label='Open...', command=self.open_profile)
        # menu_file.add_command(label='Close', command=self.close)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, send_callback=self.send_message, add_callback=self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support.
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()

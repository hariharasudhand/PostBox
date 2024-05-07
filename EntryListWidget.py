import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('200x200')

class EntryListWidget(ttk.Frame):
    """Widget that creates a column of entry boxes."""
    def __init__(self, master):
        super().__init__(master)
        self.entries = []

    def add_entry(self):
        """Creates a new entry box and keeps reference to respective variable."""
        entry_var = tk.StringVar()
        self.entries.append(entry_var)
        ttk.Entry(self, textvariable=entry_var).pack()

    def get_entries(self):
        """Gets each entrybox text and returns as list."""
        print([entry.get() for entry in self.entries])

entry_widget = EntryListWidget(root)
entry_widget.pack()

# Buttons to control adding new entry and getting their values
ttk.Button(root, text='Add Entry', command=entry_widget.add_entry).pack()
ttk.Button(root, text='Get Entries', command=entry_widget.get_entries).pack()

root.mainloop()
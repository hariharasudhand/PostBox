import tkinter as tk
from tkinter import ttk

def close_tab(event):
    # Get the index of the selected tab
    index = notebook.index("current")
    # Close the tab
    notebook.forget(index)

root = tk.Tk()
root.title("Tabbed Interface")

notebook = ttk.Notebook(root)

# Add some tabs
for i in range(5):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"Tab {i}")
    # Create a close button inside each tab
    close_button = tk.Label(tab, text="x", foreground="red", cursor="hand2")
    close_button.bind("<Button-1>", close_tab)
    close_button.place(relx=1, rely=0, anchor="ne")

notebook.pack(expand=True, fill="both")

root.mainloop()

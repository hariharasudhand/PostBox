import tkinter as tk
from tkinter import ttk

class PostBoxStyles:

    def __init__(self):
        super().__init__()
        # Create a style object
        self.style = ttk.Style()

    def load_close_btn_styles(self):
        # Create a custom style for the close button
        self.style = ttk.Style()

        # Configure the default style options for buttons
        self.style.configure("BlackRed.TButton", relief="flat", background='black', foreground='red', font=("Helvetica", 12),borderwidth = '1')
        # Map the custom style to the default button style for the entire application
        # Changes will be reflected
        # by the movement of mouse.
        self.style.map('BlackRed.TButton', foreground = [('active', '!disabled', 'black')],
                            background = [('active', 'yellow')])

        return self.style

    # Create a custom style for the Treeview widget
    def load_tree_style(self):
        
        custom_style = ttk.Style()

        # Configure the style for the Treeview
        custom_style.theme_use("clam")  # Use the 'clam' theme as the base

        # Configure the heading
        custom_style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#f0f0f0")

        # Configure the rows
        custom_style.configure("Treeview", font=("Helvetica", 10), background="#ffffff", fieldbackground="#ffffff")

        # Configure the alternating row colors
        custom_style.map("Treeview", background=[("selected", "#0078d4")])

        # Configure the selected item
        custom_style.map("Treeview", foreground=[("selected", "#ffffff")])

        # Configure the scrollbar
        custom_style.configure("Vertical.TScrollbar", gripcount=0, background="#f0f0f0", troughcolor="#ffffff")

        # Configure the tree indicators (for tree-like appearance)
        custom_style.layout("Treeview.Item", [
            ("Treeitem.padding", {"sticky": "nswe", "children": [
                ("Treeitem.indicator", {"side": "left", "sticky": ""}),
                ("Treeitem.image", {"side": "left", "sticky": ""}),
                ("Treeitem.text", {"side": "left", "sticky": ""}),
            ]}),
        ])

        return custom_style


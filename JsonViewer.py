import json
import tkinter as tk
from tkinter import messagebox, ttk


class JsonViewer:
    def __init__(self, parent_window):
        # Reference to the parent window
        self.parent_window = parent_window

    def convert_to_tree_view(self, raw_json_text_area, json_tree_view):
       
        # Read raw JSON text from the provided text area
        raw_json_text = raw_json_text_area.get(1.0, tk.END).strip()

        # Attempt to parse the raw JSON text
        try:
            json_data = json.loads(raw_json_text)
        except json.JSONDecodeError:
            # If parsing fails, show an error message and stop the function
            messagebox.showerror("Error", "The raw JSON text is not valid JSON.")
            return
        
        # Clear any existing content from the tree view
        json_tree_view.delete(*json_tree_view.get_children())

        # Display JSON data in the tree view
        self.display_json_tree(json_data, json_tree_view)

    def display_json_tree(self, data, tree, parent=''):
       
        # Recursively display JSON data as a tree-like structure
        if isinstance(data, dict):
            # Iterate through dictionary items
            for key, value in data.items():
                # Insert the key as a node in the tree view
                node = tree.insert(parent, 'end', text=key)
                # Recurse into nested data
                self.display_json_tree(value, tree, node)
        elif isinstance(data, list):
            # Iterate through list items
            for index, item in enumerate(data):
                # Insert the list index as a node in the tree view
                node = tree.insert(parent, 'end', text=f"[{index}]")
                # Recurse into nested data
                self.display_json_tree(item, tree, node)
        else:
            # Insert a leaf node with the data value
            tree.insert(parent, 'end', text=str(data))

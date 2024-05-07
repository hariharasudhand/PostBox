import tkinter as tk
from tkinter import ttk

# Create a custom style for the Treeview widget
def create_custom_tree_style():
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

def test_custom_tree_style():
    root = tk.Tk()
    root.title("Custom Treeview Style Test")

    # Create a Treeview widget
    tree = ttk.Treeview(root, style="Treeview")

    # Insert the parent item first
    parent_item = tree.insert("", "end", text="Parent", open=True)

    # Insert child items under the parent item
    tree.insert(parent_item, "end", text="Child 1")
    tree.insert(parent_item, "end", text="Child 2")
    tree.insert(parent_item, "end", text="Child 3")

    # Insert a grandchild item under the first child item
    child1_item = tree.get_children(parent_item)[0]
    tree.insert(child1_item, "end", text="Grandchild 1")

    # Apply the custom style
    custom_style = create_custom_tree_style()
    tree.configure(style="Treeview")

    # Pack the Treeview widget
    tree.pack(fill=tk.BOTH, expand=True)

    root.mainloop()




# Test the custom Treeview style
test_custom_tree_style()

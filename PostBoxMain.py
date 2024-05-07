import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, scrolledtext
import json
from HttpClient import HttpClient
from JsonViewer import JsonViewer
from DBManager import DBManager
import json
from PostBoxStyles import PostBoxStyles

class PostBoxMain(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize DBManager
        self.db_manager = DBManager()

        # Initialize header_entries as an empty list
        self.header_entries = []

        ## initiate the header row index
        self.row_index = 0;

        # Initialize styles
        self.styles = PostBoxStyles()
        self.styles.load_close_btn_styles()
        self.styles.load_tree_style()

        # Call the DBManager method to retrieve collections and requests
        self.collections_and_requests = self.db_manager.get_all_collections_and_related_requests()

        # Create the tree view widget
        self.tree = ttk.Treeview(self,style="Treeview")

         # Initialize main window
        self.title("Post~Box")
        self.request_tabs = {}
        self.request_windows = {}

        # Set window size based on screen resolution
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")

        # Initialize HttpClient
        self.http_client = HttpClient()

        # Create an instance of JsonViewer
        self.json_viewer = JsonViewer(self)

    
        # Create the main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create tree view for collections and requests
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)

        # Create a frame for the Save and Import buttons
        buttons_frame = tk.Frame(self.tree_frame)
        buttons_frame.pack(side=tk.TOP, fill=tk.X)
        # Add "S" (Save Collection) button
        save_button = tk.Button(buttons_frame, text="Save", command=self.save_collection)
        save_button.pack(side=tk.LEFT)

        # Add "I" (Import Collection) button
        import_button = tk.Button(buttons_frame, text="Import", command=self.import_collection)
        import_button.pack(side=tk.LEFT)

        # Define the delete button and set it to be initially disabled
        delete_button = tk.Button(buttons_frame, text="Delete",command=self.delete_action)

        # Pack the button in the desired location (near the save button)
        delete_button.pack(side=tk.LEFT)
        
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind tree selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create buttons for adding collections and requests
        self.button_frame = tk.Frame(self.tree_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.add_collection_button = tk.Button(self.button_frame, text="Add Collection", command=self.add_collection)
        self.add_collection_button.pack(fill=tk.X)

        self.add_request_button = tk.Button(self.button_frame, text="Add Request", command=self.add_request_panel)
        self.add_request_button.pack(fill=tk.X)
        # Initially disable the "Add Request" button
        self.add_request_button.config(state=tk.DISABLED)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        # Load collections and requests when the UI loads
        self.load_collections_and_requests()

    def add_collection(self):
        # Add a new collection to the tree view
        collection_name = simpledialog.askstring("Add Collection", "Enter collection name:")
        if collection_name:
            self.tree.insert("", "end", text=collection_name)

    def add_request_panel(self):
    
        selected_item = self.tree.focus()
        print("selected_item",selected_item)
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a collection to add a request.")
            return
        
        request_name = simpledialog.askstring("Add Request", "Enter request name:")

        # Check for duplicate request names
        children = self.tree.get_children(selected_item)
        existing_request_names = [self.tree.item(child, 'text') for child in children]
        if request_name in existing_request_names:
            messagebox.showwarning("Warning", "Duplicate request name is not allowed in the collection.")
            return
    
        if request_name:
            request_id = self.tree.insert(selected_item, "end", text=request_name)
            # Initialize tab list for the parent collection
            parent_collection = self.tree.parent(request_id)
            if parent_collection not in self.request_tabs:
                self.request_tabs[parent_collection] = []

            # Create a new request tab
            self.create_request_window(request_id,None)
           

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        match_found = False  # Add this line to track if a matching tab is found
        for collection in self.collections_and_requests:
            collection_id = collection.get('collection_id')
            requests = collection.get('requests')
            for request in requests:
                request_id = request.get('request_id')
                generated_req_id = str(collection_id) + "." + str(request_id)
                if selected_item == generated_req_id:
                    # Check if the tab for the selected request already exists
                    if generated_req_id in self.request_windows:
                        # Activate the corresponding tab in the notebook
                        request_frame = self.request_windows[generated_req_id]['frame']
                        self.notebook.select(request_frame)
                    else:
                        # If tab doesn't exist, create it
                        self.create_request_window(generated_req_id, request)
                    match_found = True
                    break
            if match_found:
                break


        # Enable or disable the "Add Request" button based on whether a collection is selected
        if selected_item:
            parent = self.tree.parent(selected_item)
            
            # If selected item is a request (has a parent)
            if parent:
                # Check if selected item is a request window that exists
                if selected_item in self.request_windows:
                    # Activate the corresponding tab in the notebook
                    request_frame = self.request_windows[selected_item]['frame']
                    self.notebook.select(request_frame)
                    
                # Only show tabs for the current collection
                current_collection = parent
                self.show_tabs(current_collection)
            
            # If selected item is a collection
            else:
                # Enable the "Add Request" button
                self.add_request_button.config(state=tk.NORMAL)
                
        else:
            # Disable the "Add Request" button if no selection
            self.add_request_button.config(state=tk.DISABLED)


    def create_request_window(self, request_id,requestData):
        
        print("requestData ----- ",requestData)
        # Set Values from DB
        methodVar = 'POST' if requestData is None else requestData.get('method', 'POST')
        #print("methodVar",methodVar)

        url_var = tk.StringVar()
        url_var.set('' if requestData is None else requestData.get('url',''))
           
        payload_var =  '' if requestData is None else requestData.get('payload','')

        headersVar = tk.StringVar()
        headersVar.set('' if requestData is None else requestData.get('headers',''))
         
        # Create a new tab for the request in the notebook
        request_frame = tk.Frame(self.notebook)
        request_name = self.tree.item(request_id, 'text')
        
        # Create a frame to hold the label and close button in the same line
        header_frame = tk.Frame(request_frame)
        header_frame.pack(fill=tk.X, pady=5)

        # Create the label for the request and pack it into the header frame
        request_label = tk.Label(header_frame, text=f"Request - {request_name}")
        request_label.pack(side=tk.LEFT)
    
        # Create a close button with the text "X" and configure its style
        # Create a close button with the text "X" and configure its style
        close_button = ttk.Button(header_frame, text="X",width=1,command=lambda: self.close_tab(request_frame), style="BlackRed.TButton")
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)  # Adjust button position and padding
     
        # Endpoint URL section
        url_label = tk.Label(request_frame, text="Endpoint URL:")
        url_label.pack(anchor='w')
        
        url_entry = tk.Entry(request_frame, width=60,textvariable=url_var)
        url_entry.pack(pady=5, anchor='w')
        
        # Add event listener to enable Send button only when URL is entered
        def on_url_change(event):
            if url_entry.get():
                send_button.config(state=tk.NORMAL)
            else:
                send_button.config(state=tk.DISABLED)
        
        url_entry.bind("<KeyRelease>", on_url_change)

        # HTTP method combobox
        method_label = tk.Label(request_frame, text="HTTP Method:")
        method_label.pack(anchor='w')

        http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        method_combobox = ttk.Combobox(request_frame, values=http_methods, state="readonly")
        method_combobox.set(methodVar)
        method_combobox.pack(pady=5, anchor='w')

        # Payload entry (for POST and other methods with payload)
        payload_label = tk.Label(request_frame, text="Payload:")
        payload_label.pack(anchor='w')
        
        payload_entry = scrolledtext.ScrolledText(request_frame, wrap='word', height=5)
        payload_entry.pack(pady=5, fill=tk.X)
        payload_entry.insert(tk.END, payload_var)  # Insert text at the end of the widget

        # Frame for headers
        headers_frame = tk.Frame(request_frame)
        headers_frame.pack(anchor='w')

        add_header_button = tk.Button(headers_frame, text="Add Header", command=lambda: self.add_header(headers_frame))
        add_header_button.pack(pady=5, anchor='w')

        # Send button
        send_button = tk.Button(request_frame, text="Send", state=tk.DISABLED, command=lambda: self.send_request(url_entry, method_combobox, payload_entry, headers_frame, request_id))
        send_button.pack(pady=5, anchor='e')

        # Create a notebook widget to manage tabs in each request frame
        request_notebook = ttk.Notebook(request_frame)
        request_notebook.pack(fill=tk.BOTH, expand=True)

        # Tab for raw JSON view
        raw_json_tab = ttk.Frame(request_notebook)
        request_notebook.add(raw_json_tab, text="Raw JSON")

        # Text widget for raw JSON view
        raw_json_text_area = scrolledtext.ScrolledText(raw_json_tab, wrap='word', height=20)
        raw_json_text_area.pack(fill=tk.BOTH, expand=True)

        # Tab for JSON tree view
        json_tree_tab = ttk.Frame(request_notebook)
        request_notebook.add(json_tree_tab, text="JSON Tree View")

        # Treeview widget for JSON tree view
        json_tree_view = ttk.Treeview(json_tree_tab)
        json_tree_view.pack(fill=tk.BOTH, expand=True)

        # Add event handler for switching tabs
        request_notebook.bind("<<NotebookTabChanged>>", lambda event, request_id=request_id: self.on_tab_change(event, request_id))

        # Store the request tab and components
        self.request_windows[request_id] = {
          "frame": request_frame,
          "url_entry": url_entry,
          "method_combobox": method_combobox,
          "payload_entry": payload_entry,
          "headers_frame": headers_frame,
          "send_button": send_button,
          "raw_json_text_area": raw_json_text_area,
          "json_tree_view": json_tree_view
        }
 
        # Add tab to notebook
        tab_index = self.notebook.add(request_frame, text=request_name)
        
        # Associate tab with request_id and its parent collection
        parent_collection = self.tree.parent(request_id)
        if parent_collection in self.request_tabs:
            self.request_tabs[parent_collection].append(request_id)

    def on_tab_change(self, event, request_id):
        # Event handler for tab changes in each request notebook
        # If the current tab is JSON tree view, convert raw JSON to tree view
        request_window = self.request_windows[request_id]
        request_notebook = event.widget
        selected_tab = request_notebook.tab(request_notebook.select(), "text")
        
        if selected_tab == "JSON Tree View":
            # Convert the raw JSON text to tree view
            raw_json_text_area = request_window["raw_json_text_area"]
            json_tree_view = request_window["json_tree_view"]
            
            self.json_viewer.convert_to_tree_view(raw_json_text_area, json_tree_view)

    def show_tabs(self, current_collection):
        # Show only tabs associated with the current collection
        if current_collection in self.request_tabs:
            tabs_to_show = self.request_tabs[current_collection]
            for tab_id in self.request_windows:
                request_frame = self.request_windows[tab_id]['frame']
                if tab_id in tabs_to_show:
                    # Show tab for the current request
                    if not self.notebook.index(request_frame):
                        self.notebook.add(request_frame)
                else:
                    # Remove tab if it does not belong to the current collection
                    if self.notebook.index(request_frame):
                        self.notebook.forget(request_frame)

    def close_tab(self, tab_id):
        print("inside close tab")
        # Get the request ID from the tab frame
        request_id = None
        for req_id, req_window in self.request_windows.items():
            if req_window['frame'] == tab_id:
                request_id = req_id
                break
        
        # If the request ID is found
        if request_id:
            # Remove the tab from the notebook
            self.notebook.forget(tab_id)

        # Remove the tab entry from request_windows dictionary
        del self.request_windows[request_id]

    def add_header(self, headers_frame):
        print("inside Add Header")
        
        # Add a new row for headers in the given headers frame
        self.row_index = len(headers_frame.pack_slaves()) // 2
        
        # Create a new frame for each header row
        header_row_frame = tk.Frame(headers_frame)
        header_row_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Key entry
        header_key_var = tk.StringVar()
        key_entry = tk.Entry(header_row_frame,textvariable=header_key_var, width=25)
        key_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Value entry
        header_value_var = tk.StringVar()
        value_entry = tk.Entry(header_row_frame,textvariable=header_value_var, width=35)
        value_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Close button
        close_button = tk.Button(header_row_frame, text="X", command=self.create_remove_header_callback(header_row_frame, self.row_index))
        close_button.pack(side=tk.LEFT)

        # Update frame configurations
        header_row_frame.pack_configure(side=tk.TOP, fill=tk.X)

        # Add the key and value entry variables to the header_entries list
        self.header_entries.append((header_key_var, header_value_var))

    def create_remove_header_callback(self, header_row_frame, index):
        return lambda: self.remove_header(header_row_frame, index)

    def remove_header(self, header_row_frame, row_index):
        # Remove the widgets in the specified row
        header_row_frame.destroy()

    def send_request(self, url_entry, method_combobox, payload_entry, headers_frame, request_id):

        key_entry = None  # Initialize key_entry here to avoid UnboundLocalError
        # Get the URL, method, and payload from the form
        url = url_entry.get()
        method = method_combobox.get()
        payload = payload_entry.get(1.0, tk.END).strip()
        # Gather headers from the form
        headers = {}
        total_rows = self.row_index+1

        print("elf.row_index",total_rows)

        for key_var, value_var in self.header_entries:
            print("key_var:", key_var.get())
            print("value_var:", value_var.get())

        print("headers", headers)
        # Use the HttpClient to send the request
        try:
            response_text = self.http_client.send_request(url, method, payload, headers)
            
            # Access the raw JSON text area from the request window
            raw_json_text_area = self.request_windows[request_id]["raw_json_text_area"]
            # Display the response in the text area
            raw_json_text_area.delete(1.0, tk.END)
            raw_json_text_area.insert(tk.END, response_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
      

    def load_collections_and_requests(self):
        
        # Check if there are collections and requests to process
        if self.collections_and_requests:
            # Iterate through each collection
            for collection in self.collections_and_requests:
                collection_id = collection.get('collection_id')
                collection_name = collection.get('collection_name')
                #print("collection_name = "+ collection_name+"  collection_id = "+str(collection_id))
                # Ensure the collection has a name
                if collection_name:
                    # Add the collection to the tree view
                    collection_node = self.tree.insert('', 'end', text=collection_name, iid=collection_id)
                    
                    # Retrieve requests associated with the current collection
                    requests = collection.get('requests')
                    #print(requests)
                    # Check if there are any requests
                    if requests:
                        # Iterate through each request in the current collection
                        for request in requests:
                            #print()
                            #print("request",request)
                            # Parse request data
                            #request_data = json.loads(request)
                            
                            # Extract request details
                            request_id = request.get('request_id')
                            request_name = request.get('request_name')
                            #print("---- adding tab with request_id",request_id)
                            # Add the request as a child node under the collection node
                            generated_request_id = str(collection_id)+"."+str(request_id)
                            req_node = self.tree.insert(collection_node, 'end', text=request_name, iid=generated_request_id)

                            # Bind click event to the request node
                            #self.create_request_window(req_node,request)


    def save_collection(self):
        # Loop through each collection in the tree view
        for collection_id in self.tree.get_children():
            # Retrieve collection name
            collection_name = self.tree.item(collection_id, 'text')
            #print("SAving Collection",collection_name)
            # Save the collection to the database and get the collection ID
            db_collection_id = self.db_manager.add_collection(collection_name)
            
            # Loop through each request under the collection
            for request_id in self.tree.get_children(collection_id):
                # Retrieve request data
                request_name = self.tree.item(request_id, 'text')
                
                #print("retriving request_windows for request_id : ",request_id)
                # Retrieve the request data from the request_windows dictionary
                request_window = self.request_windows[request_id]
                #print("request_window['method_combobox']",request_window['method_combobox'])
                method = request_window['method_combobox'].get()
                url = request_window['url_entry'].get()
                payload = request_window['payload_entry'].get(1.0, tk.END).strip()
                
                # Retrieve headers from the headers frame
                headers = {}
                for child in request_window['headers_frame'].winfo_children():
                    entries = child.winfo_children()
                    if len(entries) == 2:
                        key_entry, value_entry = entries
                        key = key_entry.get()
                        value = value_entry.get()
                        if key and value:
                            headers[key] = value
                
                #print("request_name",request_name)
                #print("db_collection_id",db_collection_id)
                #print("url",url)
                #print("method",method)
                #print("payload",payload)
                #print("headers",json.dumps(headers))
                # Save the request to the database
                self.db_manager.add_request(
                    request_name,
                    db_collection_id,
                    url,
                    method,
                    payload,
                    json.dumps(headers)
                )
            
        # Show a success message
        messagebox.showinfo("Success", "Collections and requests saved successfully.")

    def import_collection(self):
        # Import a collection and requests from a file
        file_path = simpledialog.askstring("Import Collection", "Enter the file path of the collection to import:")
        
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Get the collection name
                collection_name = data['collection_name']
                
                # Add the collection to the tree view
                collection_id = self.tree.insert("", "end", text=collection_name)
                
                # Add requests to the tree view
                for request in data['requests']:
                    request_name = request['name']
                    request_id = self.tree.insert(collection_id, "end", text=request_name)
                    
                    # Create the request window
                    self.create_request_window(request_id)

    def delete_action(self):
        selected_item = self.tree.focus()
        print("selected_item",selected_item)
        result = selected_item.split(".")[1] if "." in selected_item else selected_item
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a collection or request to delete.")
            return
        
        if(self.db_manager.isID_A_CollectionType(result)) :
            self.db_manager.delete_collection(int(result))
        else:
            
            self.db_manager.delete_request(int(result))
        
        # Remove the corresponding item from the tree view
        self.tree.delete(selected_item)
        # Remove the request window from the dictionary
        if selected_item in self.request_windows:
            del self.request_windows[selected_item]

        
if __name__ == "__main__":
    app = PostBoxMain()
    app.mainloop()

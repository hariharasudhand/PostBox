import sqlite3

class DBManager:
    def __init__(self, db_path='postbox.db'):
        # Initialize a connection to the SQLite database
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        # Create the tables if they do not exist
        self.create_tables()

    def create_tables(self):
        # Create collections table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create requests table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                collection_id INTEGER,
                url TEXT,
                method TEXT,
                payload TEXT,
                headers TEXT,
                FOREIGN KEY (collection_id) REFERENCES collections (id)
            )
        ''')

        # Commit changes
        self.connection.commit()

    def add_collection(self, collection_name):
     
        # Add a new collection to the database
        self.cursor.execute('''
            INSERT INTO collections (name)
            VALUES (?)
            ''', (collection_name,))
        self.connection.commit()

        # Return the ID of the added collection
        return self.cursor.lastrowid

    def add_request(self, request_name, collection_id, url, method, payload, headers):
        print("inside add request",request_name)
        # Add a new request to the database
        self.cursor.execute('''
            INSERT INTO requests (name, collection_id, url, method, payload, headers)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (request_name, collection_id, url, method, payload, headers))
        self.connection.commit()

        # Return the ID of the added request
        return self.cursor.lastrowid

    def delete_collection(self, collection_id):
        # Delete a collection from the database
        self.cursor.execute('''
            DELETE FROM collections WHERE collection_id = ?
        ''', (collection_id,))

        # Also delete associated requests
        self.cursor.execute('''
            DELETE FROM requests WHERE collection_id = ?
        ''', (collection_id,))
        self.connection.commit()

    def delete_request(self, request_id):
        # Delete a request from the database
        self.cursor.execute('''
            DELETE FROM requests WHERE request_id = ?
        ''', (request_id,))
        self.connection.commit()

    def get_collections(self):
        # Retrieve all collections from the database
        self.cursor.execute('''
            SELECT * FROM collections
        ''')
        return self.cursor.fetchall()

    def get_requests_by_collection(self, collection_id):
        # Retrieve all requests for a given collection from the database
        self.cursor.execute('''
            SELECT * FROM requests WHERE collection_id = ?
        ''', (collection_id,))
        return self.cursor.fetchall()

    def get_all_collections_and_related_requests(self):
        # Query to join collections and requests and retrieve their data
        self.cursor.execute('''
            SELECT collections.collection_id, collections.name AS collection_name,
                   requests.request_id, requests.name AS request_name,
                   requests.method, requests.url, requests.payload, requests.headers
            FROM collections
            LEFT JOIN requests ON collections.collection_id = requests.collection_id
            ORDER BY collections.collection_id, requests.request_id
        ''')
        
        # Fetch all results
        rows = self.cursor.fetchall()
        
        # Initialize a dictionary to store collections and related requests
        collections_and_requests = {}
        
        # Process the rows to group requests under their respective collections
        for row in rows:
            collection_id = row[0]
            collection_name = row[1]
            request_id = row[2]
            request_name = row[3]
            request_method = row[4]
            request_url = row[5]
            request_payload = row[6]
            request_headers = row[7]
            
            # Check if the collection is already in the dictionary
            if collection_id not in collections_and_requests:
                collections_and_requests[collection_id] = {
                    'collection_id': collection_id,
                    'collection_name': collection_name,
                    'requests': []
                }
            
            # Add request data to the requests list for the collection
            if request_id is not None:
                collections_and_requests[collection_id]['requests'].append({
                    'request_id': request_id,
                    'request_name': request_name,
                    'method': request_method,
                    'url': request_url,
                    'payload': request_payload,
                    'headers': request_headers
                })

        # Convert the dictionary to a list of dictionaries for easier processing
        result = list(collections_and_requests.values())
        
        # Return the list of collections and their related requests
        return result
    
    def isID_A_CollectionType(self, id):
        # Check if the given ID exists in the collections table
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM collections
            WHERE collection_id = ?
        ''', (id,))
        
        # Fetch the count of matching records in the collections table
        count_in_collections = self.cursor.fetchone()[0]
        
        # If the ID exists in the collections table, it is a collection ID
        if count_in_collections > 0:
            return True  # The ID belongs to a collection

        # Check if the given ID exists in the requests table
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM requests
            WHERE request_id = ?
        ''', (id,))
        
        # Fetch the count of matching records in the requests table
        count_in_requests = self.cursor.fetchone()[0]
        
        # If the ID exists in the requests table, it is a request ID
        if count_in_requests > 0:
            return False  # The ID belongs to a request
        
        # If the ID does not exist in either the collections or requests table, raise an exception
        #raise ValueError(f"No record found with ID {id} in collections or requests.")

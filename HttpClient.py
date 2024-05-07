import requests

class HttpClient:
    def send_request(self, url, method, payload=None, headers=None):
        """
        Sends an HTTP request and returns the response text.

        Parameters:
        - url (str): The URL to send the request to.
        - method (str): The HTTP method to use (GET, POST, PUT, DELETE, PATCH).
        - payload (str, optional): The request payload for POST, PUT, PATCH methods. Defaults to None.
        - headers (dict, optional): The request headers. Defaults to None.

        Returns:
        - str: The response text from the HTTP request.
        """
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, data=payload)
            elif method == "PUT":
                response = requests.put(url, headers=headers, data=payload)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, data=payload)
            
            # Return the response text
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while making the request: {str(e)}")

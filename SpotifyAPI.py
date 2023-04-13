import os
import requests
import base64
from urllib.parse import urlencode
from datetime import datetime
from flask import session, current_app



class SpotifyAPI_InstanceClass:
    """This clase us particularly useful at testing it with iPython while developing the app.
    It contains all the procedures required to communicate with Spotify's API"""

    def __init__(self, client_id, secret):
        
        self.client_id = client_id
        self.secret = secret
        self.token_data = {"grant_type": "client_credentials"} #can be passed as an optional argument
        """URL addresses"""
        self.url_redirect = "http://127.0.0.1:5000/home.html"
        self.url_authorize = "https://accounts.spotify.com/authorize"
        self.url_token = "https://accounts.spotify.com/api/token"
        self.url_search = "https://api.spotify.com/v1/search"
        self.url_base = "https://api.spotify.com/v1"
        self.timestamp = datetime.utcnow()

    ###### AUTH SECTION ######

    def create_token_header(self):
        """Create required TOKEN under its parameters
        They should be encoded into a base64"""

        client_creds = f"{self.client_id}:{self.secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return {
           "Authorization": f"Basic {client_creds_b64.decode()}"
            }

    def get_client_credentials_token(self):
        """Sends the credentials to the API to get a valid token for an hour
        updates the class instance with the parameters if the request is succesful"""
        resp = requests.post(
            self.url_token,
            data=self.token_data,
            headers= self.create_token_header()
        )

        if resp.status_code == 200:
            resp_data = resp.json()
            self.access_token = resp_data['access_token']
            self.token_type = resp_data['token_type']
            self.expires_in = resp_data['expires_in']
            return resp_data
        else: 
            return resp

    ###### API SEARCH SECTION ######
    """"Retrieves results according to the specified type of item"""

    def current_headers(self):
        """Retrieve the headers in the correct format"""
        return {
         "Authorization": f"Bearer {self.access_token}"   
        }


    def search_item(self, query_string, item_type, limit=5, offset=0):
        """Connects to the search endpoint and """

        query_data = urlencode({
            "q": f"{query_string}",
            "type" : f"{item_type}",
            "limit" : f"{limit}",
            "offset" : f"{offset}"
            })
        search_url = f"{self.url_search}?{query_data}"
        resp = requests.get(search_url, headers=self.current_headers())

        if resp.status_code == 200:
            resp_data = resp.json()
            print("200 ok")
            return resp_data
        
        elif resp.status_code == 401:
            """if the token is expired renew the token and re attempt the request"""
            self.get_client_credentials_token()
            resp = requests.get(search_url, headers=self.current_headers())
            resp_data = resp.json()
            return resp_data 
        
        else:
            return resp
    
    ##### API GET ITEMS SECTION #####

    def get_item(self, item_type, spotify_id):
        """Retrieves the item from Spotify's API """

        url_for_item = f"{self.url_base}/{item_type}/{spotify_id}"
        resp = requests.get(url_for_item, headers=self.current_headers())

        if resp.status_code == 401: #will this conduct to an inifinite loop?
            """if the token is expired renew the token and re attempt the request"""
            self.get_client_credentials_token()
            resp = requests.get(url_for_item, headers=self.current_headers())
        
        return resp


###########################################################

class SpotifyAPI:
    """All the procedures required to communicate with Spotify's API"""
    
    client_id = os.environ.get('API_CLIENT_ID')
    secret = os.environ.get('API_SECRET')
    token_data = {"grant_type": "client_credentials"}
    """URL addresses"""
    url_redirect = "http://127.0.0.1:5000/home.html"
    url_authorize = "https://accounts.spotify.com/authorize"
    url_token = "https://accounts.spotify.com/api/token"
    url_base = "https://api.spotify.com/v1"

    ################## AUTH SECTION ##################

    @classmethod
    def create_token_header(cls):
        """Create required TOKEN under its parameters
        They should be encoded into a base64"""

        client_creds = f"{cls.client_id}:{cls.secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return {
           "Authorization": f"Basic {client_creds_b64.decode()}"
            }

    @classmethod
    def get_client_credentials_token(cls):
        """Sends the credentials to the API to get a valid token for an hour
        updates the class instance with the parameters if the request is succesful"""
        resp = requests.post(
            cls.url_token,
            data=cls.token_data,
            headers= cls.create_token_header()
            )
        print('¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞ this is resp', resp)
        if resp.status_code == 200:
            print('******************************************** TOKEN CREATED')
            resp_data = resp.json()
            return resp_data
        
        return False


    @classmethod
    def current_headers(cls):
        """Retrieve the headers in the correct format."""
        return {
         "Authorization": f"Bearer {session['SPOTIFY_COMMENTS_API_TOKEN']}"   
        }


    @classmethod
    def credentials_in_session(cls):
        """Validates credentials for the first time and stores the data in the session"""

        result = cls.get_client_credentials_token()
        if result:
            session['SPOTIFY_COMMENTS_API_TOKEN'] = result['access_token']
            session['SPOTIFY_COMMENTS_TOKEN_TYPE'] = result['token_type']
            session['SPOTIFY_COMMENTS_EXPIRES_IN'] = result['expires_in']
        
        elif result == False: #don't really know if this is necessary to maintain
            print("Token is false")

    @classmethod
    def check_auth(cls):
        """This will check if there's already a API token in the user session"""
        if not 'SPOTIFY_COMMENTS_API_TOKEN' in session:
            cls.credentials_in_session()

            
    ################## API SEARCH SECTION ##################

    @classmethod
    def search_item(cls, query_string, item_type, limit=5, offset=0):
        """Connects to the search endpoint and returns response. Revalidates
        credentials if the token has expired and return the response. """

        query_data = urlencode({
            "q": f"{query_string}",
            "type" : f"{item_type}",
            "limit" : f"{limit}",
            "offset" : f"{offset}"
            })
        search_url = f"{cls.url_base}/search?{query_data}"
        
        
        resp = requests.get(search_url, headers=cls.current_headers())
        
        if resp.status_code == 401: #will this conduct to an inifinite loop?
            """if the token is expired renew the token and re attempt the request"""
            cls.credentials_in_session()
            resp = requests.get(search_url, headers=cls.current_headers())

        return resp
    
    @classmethod
    def get_item(cls, item_type, spotify_id):
        """Retrieves the item from Spotify's API """

        url_for_item = f"{cls.url_base}/{item_type}/{spotify_id}"

        resp = requests.get(url_for_item, headers=cls.current_headers())

        if resp.status_code == 401: #will this conduct to an inifinite loop?
            """if the token is expired renew the token and re attempt the request"""
            cls.credentials_in_session()
            resp = requests.get(url_for_item, headers=cls.current_headers())
        
        return resp
  




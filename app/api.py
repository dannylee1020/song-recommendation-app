import datetime
import json
import requests
from urllib.parse import urlencode
import base64
import config


class SpotifyAPI(object):
  client_id = None
  client_secret = None
  access_token = None
  access_token_expires = datetime.datetime.now()
  access_token_did_expire = True


  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret


# getting client credentials needed for auth
  def get_client_credentials(self):
    """
    Returns a base64 encoded string
    """
    client_id = self.client_id
    client_secret = self.client_secret
    client_creds = f"{client_id}:{client_secret}"

    if client_id == None or client_secret == None:
      raise("Please set client_id and client_secret")

    client_creds_b64 = base64.b64encode(client_creds.encode())
    return client_creds_b64.decode()
    

# headers for auth
  def get_token_headers(self):
    client_creds_b64 = self.get_client_credentials()
    headers = {
        'Authorization':f"Basic {client_creds_b64}"
    }

    return headers

# data for auth
  def get_token_data(self):
    token_data = {
      'grant_type':'client_credentials'
        }

    return token_data

# method to perform auth
  def perform_auth(self):

    token_headers = self.get_token_headers()
    token_data = self.get_token_data()
    r = requests.post(config.AUTH_URL, data = token_data, headers = token_headers)

    if r.status_code not in range(200, 299):
      raise Exception('Authentication Failed')

    data = r.json()
    now = datetime.datetime.now()
    expires_in = data['expires_in'] # seconds
    expires = now + datetime.timedelta(seconds = expires_in)
    self.access_token_expires = expires
    self.access_token_did_expire = expires < now

    access_token = data['access_token']
    self.access_token = access_token

    return True

# getting access token from performing auth
  def get_access_token(self):
    token = self.access_token
    expires = self.access_token_expires
    now = datetime.datetime.now()

    if expires < now:
      self.perform_auth()
      return self.get_access_token()

    elif token == None:
      self.perform_auth()
      return self.get_access_token()

    return token

# header for getting data from web api
  def get_resource_header(self):
    access_token = self.get_access_token()
    headers = {
    'Authorization':f"Bearer {access_token}"
    }
    return headers

# basic search method
  def base_search(self,query_params):
    endpoint = 'https://api.spotify.com/v1/search'
    lookup_url = f"{endpoint}?{query_params}"
    r = requests.get(lookup_url, headers = self.get_resource_header())

    if r.status_code not in range(200,299):
      return {}

    return r.json()


# robust search method
  def search(self, query=None, operator=None, operator_query=None, search_type='track'):
    if query == None:
      raise Exception('A query is required')
    
    if isinstance(query,dict):
      query = ' '.join([f"{k}:{v}" for k,v in query.items()])

    if operator != None and operator_query != None:
      if operator.lower() == 'or' or operator.lower() == 'not':
        operator = operator.upper()
        if isinstance(operator_query,str):
          query = f"{query} {operator} {operator_query}"
    
    query_params = urlencode({'q':query, 'type':search_type.lower()})

    search_result = self.base_search(query_params)
    if search_result[f"{search_type}s"]['total'] == 0:
      print('Song not found on Spotify.')
    else:
      return self.base_search(query_params)


# get artist and track id using search
  def get_id(self, query=None, operator=None, operator_query=None):
    '''
    returns corresponding artist and track id from search
    '''

    if query == None:
      raise Exception('A query is required')

    search_result = self.search(query, operator, operator_query, search_type = 'track')
    if search_result != None:
      artist_id = search_result['tracks']['items'][0]['artists'][0]['id']
      track_id = search_result['tracks']['items'][0]['id']
      return artist_id, track_id
    else:
      return



# recommendation based on input song
  def get_recommendation(self, artist=None, track=None, version = 'v1'):
    endpoint = f"https://api.spotify.com/{version}/recommendations"
    headers = self.get_resource_header()
    if artist == None or track == None:
      raise Exception('artist and track name is required')
      
    query = {'artist':artist, 'track':track}

    if self.get_id(query) != None:
      seed_artist, seed_track = self.get_id(query)
      query_param = urlencode({'seed_artists':seed_artist, 'seed_tracks':seed_track})
      lookup_url = f"{endpoint}?{query_param}"

      r = requests.get(lookup_url, headers = headers)
      data = r.json()

      names = [i['name'] for i in data['tracks']]
      item = [i for i in data['tracks']]

      # getting artist names
      artists = []
      for i in range(len(item)):
        artist_names = item[i]['artists'][0]['name']
        artists.append(artist_names)
      
      # gettin album names
      albums = []
      for i in range(len(item)):
        album_names = item[i]['album']['name']
        albums.append(album_names)

      
      result = list(zip(names, artists))
      recommendation = []
      for i in result:
        rec = f"{i[0]} -- {i[1]}"
        recommendation.append(rec)
      
      return recommendation   

    else:
      return 


      

import pandas as pd
import requests
import json
import networkx as nx

import os

from modules import config
from modules import plotting


def github_request_by_url(url):
    ''' This function allows any request using any url.
    Common endpoints for this project:
    "https://api.github.com/users/"
    "https://api.github.com/rate_limit"
    "https://api.github.com/users/{user}/following"
    
    '''
    # make the get request
    r = requests.get(url, auth=(username,token))
    
    # unpack and return
    return json.loads(r.content)


# General purpose github_request function, that can handle any endpoint or user combination.
def github_request(user, endpoint = None):
    ''' Function to retrieve user details.
    If endpoint = None, then it will retrieve user info. 
    If endpoint is set to 
    "following", 
    "followers", 
    "repos", 
    "subscriptions",
    "events", etc it will handle those requests as such. '''
    # url for get request 
    if endpoint is not None:
        url = f'https://api.github.com/users/{user}/{endpoint}'
        #print(f"Requesting {url}")
    else:
        url = f'https://api.github.com/users/{user}'
        #print(f"Requesting {url}")
    
    # make the get request
    r = requests.get(url, auth=(username,token))
    if r.status_code != 200:
        print("Something went wrong.")
    # unpack and return
    return json.loads(r.content)


# Generate a user details dictionary by extracting
def generate_user_details_dict(user):
    ''' Function generates a dictionary for a specific user. 
    
    This combines user details and users following.'''
    
    # First we need to get the users details
    user_details_dict = github_request(user)

    # Add user_following_list login names to user_details_dict as a key:value pair (login:list of logins)
    user_details_dict['following_users'] = [user['login'] for user in github_request(user, endpoint = 'following')]
    user_details_dict['followers_users'] = [user['login'] for user in github_request(user, endpoint = 'followers')]
    
    return user_details_dict


# Generates a list of dictionaries with details 
#  for all users followed by the original user.
def return_following_details_list(user):
    users_details_list = []
    users_login_set = set(user)
    users_details_list.append(generate_user_details_dict(user))
    
    # Loop over all users following and generate their own user details dictionaries.
    for fol_user in users_details_list[0]['following_users']:
        print(fol_user)
        users_login_set.add(fol_user)
        users_details_list.append(generate_user_details_dict(fol_user))
        users_login_set.add
        
    return users_details_list
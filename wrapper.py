import os

import requests
from dotenv import load_dotenv

from utils import handle_response

load_dotenv()


class ClickUpAPI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("CLICKUP_API_KEY")
        if not self.api_key:
            raise ValueError("ClickUp API key is required. Provide it or set CLICKUP_API_KEY environment variable.")
        
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    @handle_response
    def get(self, endpoint:str=None, params: dict = {}):
        if not endpoint:
            return None
        
        params = params or {}
        response = requests.get(
            url=f"{self.base_url}/{endpoint.lstrip('/')}", 
            headers=self.headers, 
            params=params
        )

        return response

    @handle_response
    def put(self, endpoint: str = None, data: dict = None, json_data: dict = None):
        if not endpoint:
            return None
        
        kwargs = {"headers": self.headers}
        if json_data:
            kwargs["json"] = json_data
        elif data:
            kwargs["data"] = data
            
        response = requests.put(
            url=f"{self.base_url}/{endpoint.lstrip('/')}", 
            **kwargs
        )

        return response

    @handle_response
    def delete(self, endpoint: str = None):
        if not endpoint:
            return None
            
        response = requests.delete(
            url=f"{self.base_url}/{endpoint.lstrip('/')}", 
            headers=self.headers
        )

        return response

    

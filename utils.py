import requests
from functools import wraps


class ClickUpAPIError(Exception):
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


def handle_response(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        method_name = func.__name__.upper()
        
        try:
            response = func(self, *args, **kwargs)
            
            if response is None:
                raise ClickUpAPIError("Invalid endpoint provided")
            
            return _process_response(response, method_name)
            
        except requests.exceptions.RequestException as e:
            print(f"ClickUp API {method_name} request failed: {str(e)}")
            raise ClickUpAPIError(f"Request failed: {str(e)}")
        
        except ClickUpAPIError:
            raise
            
        except Exception as e:
            print(f"ClickUp API {method_name} unexpected error: {str(e)}")
            raise ClickUpAPIError(f"Unexpected error: {str(e)}")
    
    return wrapper


def _process_response(response: requests.Response, method_name: str):    
    try:
        response_data = response.json() if response.content else {}
    except ValueError:
        response_data = {"raw_response": response.text}
    
    if 200 <= response.status_code < 300:
        if response.status_code == 204 or not response_data:
            return {"success": True, "status_code": response.status_code}
        
        return response_data
    
    elif 400 <= response.status_code < 500:
        error_msg = _extract_error_message(response_data, response.status_code)
        
        if response.status_code == 401:
            print("ClickUp API authentication failed")
            raise ClickUpAPIError("Authentication failed - check your API key", response.status_code, response_data)
        
        elif response.status_code == 403:
            print("ClickUp API access forbidden")
            raise ClickUpAPIError("Access forbidden - insufficient permissions", response.status_code, response_data)
        
        elif response.status_code == 404:
            print(f"ClickUp API resource not found: {response.url}")
            raise ClickUpAPIError("Resource not found", response.status_code, response_data)
        
        elif response.status_code == 429:
            print("ClickUp API rate limit exceeded")
            raise ClickUpAPIError("Rate limit exceeded", response.status_code, response_data)
        
        else:
            print(f"ClickUp API client error: {error_msg}")
            raise ClickUpAPIError(error_msg, response.status_code, response_data)
    else:
        error_msg = f"Server error: {response.status_code}"
        print(f"ClickUp API server error: {error_msg}")
        raise ClickUpAPIError(error_msg, response.status_code, response_data)


def _extract_error_message(response_data: dict, status_code: int) -> str:
    if isinstance(response_data, dict):
        for field in ['err', 'error', 'message', 'detail']:
            if field in response_data:
                return str(response_data[field])
        
        if 'ECODE' in response_data:
            return f"ClickUp Error Code: {response_data['ECODE']}"
    
    return f"HTTP {status_code} error"
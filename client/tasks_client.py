# api_client.py
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        # self.api_key = api_key
    
    def get_all_tasks(self,endpoint):
        # headers = {'Authorization': f''}
        response = requests.get(f'{self.base_url}/{endpoint}')
        return response.json()

#     def make_request(self, endpoint, params=None):
#         headers = {'Authorization': f'Bearer {self.api_key}'}
#         response = requests.get(f'{self.base_url}/{endpoint}', params=params, headers=headers)
#         response.raise_for_status()
#         return response.json()

# # data_models.py
# class UserData:
#     def __init__(self, user_id, username):
#         self.user_id = user_id
#         self.username = username

# # service_layer.py
# class UserService:
#     def __init__(self, api_client):
#         self.api_client = api_client

#     def get_user_data(self, user_id):
#         endpoint = f'users/{user_id}'
#         data = self.api_client.make_request(endpoint)
#         return UserData(user_id=data['id'], username=data['username'])

# main.py
if __name__ == '__main__':
    base_url = 'http://0.0.0.0:80'
    # api_key = 'your_api_key'
    
    api_client = APIClient(base_url)
    # user_service = UserService(api_client)
    
    # user_id = 123
    # user_data = user_service.get_user_data(user_id)
    # print(f'User ID: {user_data.user_id}, Username: {user_data.username}')
    tasks = api_client.get_all_tasks('tasks/')
    print(tasks)


# import requests

# class APIClient:
#     def __init__(self, base_url, access_token=None):
#         self.base_url = base_url
#         self.access_token = access_token

#     def set_access_token(self, access_token):
#         self.access_token = access_token

#     def _get_headers(self):
#         headers = {}
#         if self.access_token:
#             headers['Authorization'] = f'Bearer {self.access_token}'
#         return headers

#     def get_all_tasks(self, endpoint):
#         headers = self._get_headers()
#         response = requests.get(f'{self.base_url}/{endpoint}', headers=headers)
#         return response.json()


# from api_client import APIClient

# # Initialize the client with the base URL
# api_client = APIClient(base_url='https://your-api-base-url')

# # Log in and get the access token
# login_payload = {
#     'username': 'your_username',
#     'password': 'your_password',
# }

# login_response = requests.post('https://your-api-base-url/token', data=login_payload)
# access_token = login_response.json().get('access_token')

# # Set the access token in the client
# api_client.set_access_token(access_token)

# # Now you can make authenticated requests
# tasks = api_client.get_all_tasks('tasks')
# print(tasks)

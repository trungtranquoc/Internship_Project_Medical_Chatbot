import httpx
from httpx import AsyncClient
from exception import ConnectionError, CustomHTTPError

def handle_http_exceptions(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except httpx.HTTPStatusError as e:
            # Raise custom HTTP error based on status code
            CustomHTTPError.error_raising(e.response.status_code, str(e))
        except httpx.ConnectError as e:
            # Raise custom connection error
            raise ConnectionError(self.client.base_url, str(e))
        except Exception as e:
            raise CustomHTTPError.error_raising(500, str(e))
    return wrapper


class HTTPClient:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = 20):
        print(f"Initializing HTTPClient with base_url: {base_url}, headers: {headers}, timeout: {timeout}")
        self.client = AsyncClient(base_url=base_url, headers=headers)
        self.client.timeout = timeout

    async def ping(self):
        print("Checking connection to the backend server...")
        ping_response = await self.client.post("/ping")
        if ping_response.status_code != 200:
            raise ConnectionError(self.client.base_url, ping_response.status_code)

    def set_user_header(self, user_id: str):
        self.client.headers.update({"user_id": user_id})

    @handle_http_exceptions
    async def login(self, username: str, password: str):
        login_response = await self.client.post("/login", json={"username": username, "password": password})
        login_response.raise_for_status()
        return login_response.json()

    @handle_http_exceptions
    async def get(self, endpoint: str, params: dict = None):
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    @handle_http_exceptions
    async def post(self, endpoint: str, body: dict = None):
        response = await self.client.post(endpoint, json=body)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
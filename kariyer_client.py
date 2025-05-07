import requests
from typing import Optional
from search_models import Response

class KariyerSearch:
    def __init__(self, auth_token: str):
        self.base_url = "https://candidatesearchapigateway.kariyer.net/search"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def search(self, member_id: int, page: int = 1, size: int = 5, url: str = "") -> Optional[Response]:
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "memberId": member_id,
                    "currentPage": page,
                    "size": size,
                    "url": url
                }
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None 
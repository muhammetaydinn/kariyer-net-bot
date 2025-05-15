import requests
from typing import Optional
from src.models.search_models import Response

class KariyerSearch:
    def __init__(self, auth_token: str):
        self.base_url = "https://candidatesearchapigateway.kariyer.net/search"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def search(self, member_id: int, page: int = 1, keyword: str = None, isIstanbul: bool = True) -> Optional[Response]:
        try:
            # Base request body
            request_body = {
                "date":["3"],
                "memberId": member_id,
                "currentPage": page,
                "size": 50,
                "workTypes": ["1"],  # full time
                "handicappedStatus": "30",  # engelli olmayan
                "dontShowAppliedJobs": True,  # basvurduğum ilanları gösterme
                "departments": ["2", "5", "22", "55", "63", "78"]
            }

            # Add keyword if provided
            if keyword:
                request_body["keyword"] = keyword
            # Add location or workModels based on isIstanbul
            if isIstanbul:
                request_body["location"] = {"cities": ["998", "34", "82"]}  # istanbul tümü, istanbul avrupa, istanbul asya
            else:
                request_body["workModels"] = ["1"]  # remote

            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=request_body
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None 
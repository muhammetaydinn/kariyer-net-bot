import requests
from typing import Optional
from src.models.job_detail_models import JobDetailResponse

class JobDetailClient:
    def __init__(self, auth_token: str):
        self.base_url = "https://api-web.kariyer.net/jb/v1/api/jobs/jobdetail/candidateinformation"
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {auth_token}",
            "clienttype": "1",
            "origin": "https://www.kariyer.net",
            "referer": "https://www.kariyer.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

    def get_job_detail(self, job_id: int) -> Optional[JobDetailResponse]:
        try:
            response = requests.get(
                f"{self.base_url}?jobId={job_id}",
                headers=self.headers,
                verify=True
            )
            response.raise_for_status()
            return JobDetailResponse(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None 
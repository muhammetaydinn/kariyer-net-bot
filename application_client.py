import logging
import requests
from typing import Optional, Dict, Any
from application_models import ApplicationBody

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApplicationClient:
    def __init__(self, auth_token: str):
        self.base_url = "https://candidatewebapigw.kariyer.net/jobapplications"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {auth_token}",
            "ClientType": "1",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.kariyer.net",
            "Referer": "https://www.kariyer.net"
        }
        self.last_error_text = None

    def apply(self, body: ApplicationBody) -> Optional[Dict[str, Any]]:
        """İş başvurusu yapar."""
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=body.to_dict(),
                verify=True
            )
            response.raise_for_status()
            self.last_error_text = None
            return response.json()

        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                self.last_error_text = e.response.text
                # Sadece "daha önce başvuru yapıldı" hatası değilse logla
                if "Bu ilana daha önce başvuru yaptın" not in e.response.text:
                    logger.error(f"Error applying to job: {e}")
                    logger.error(f"Response text: {e.response.text}")
            return None 
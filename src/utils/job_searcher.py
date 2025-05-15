from src.clients.kariyer_client import KariyerSearch
from src.clients.job_detail_client import JobDetailClient
from src.services.job_manager import JobManager
import time

class JobSearcher:
    def __init__(self, auth_token: str, member_id: int):
        self.auth_token = auth_token
        self.member_id = member_id
        self.kariyer = KariyerSearch(auth_token)
        self.client = JobDetailClient(auth_token)
        self.job_manager = JobManager(auth_token)

    def search_and_process_jobs(self):
        self._search_istanbul_jobs()
        self._search_remote_jobs()

    def _search_istanbul_jobs(self):
        print("\nSearching in Istanbul...")
        page = 1
        while True:
            print(f"\nProcessing page {page}")  
            search_result = self.kariyer.search(
                self.member_id,
                page=page,
                isIstanbul=True,
            )
            
            if not self._process_search_results(search_result, page, "Istanbul"):
                break
                
            time.sleep(2)
            page += 1

    def _search_remote_jobs(self):
        print("\nSearching for remote jobs...")
        page = 1
        while True:
            print(f"\nProcessing page {page}")  
            search_result = self.kariyer.search(
                self.member_id,
                page=page,
                isIstanbul=False,
            )
            
            if not self._process_search_results(search_result, page, "remote"):
                break
                
            time.sleep(2)
            page += 1

    def _process_search_results(self, search_result, page: int, location: str) -> bool:
        if not search_result or not search_result.data.jobs.items:
            print(f"No more {location} jobs found")
            return False
            
        # Process jobs
        filtered_jobs = [
            job for job in search_result.data.jobs.items 
            if str(job.id) not in self.job_manager.applied_jobs 
            and str(job.id) not in self.job_manager.failed_jobs
        ]
        
        if not filtered_jobs:
            print(f"No new jobs found on page {page}")
            return True
            
        print(f"Found {len(filtered_jobs)} new jobs on page {page}")
        
        # Process each job
        for job in filtered_jobs:
            job_detail = self.client.get_job_detail(job_id=job.id)
            if not job_detail:
                continue
                
            self.job_manager.process_job(job.id, search_result, job_detail)
            time.sleep(1)
            
        return True 
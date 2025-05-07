from kariyer_client import KariyerSearch
from job_detail_client import JobDetailClient
from job_manager import JobManager
import time

def main():
    auth_token = "<auth_token>"
    kariyer = KariyerSearch(auth_token)
    client = JobDetailClient(auth_token)
    job_manager = JobManager(auth_token)
    
    # Search for jobs
    search_result = kariyer.search(member_id=26991322, size=50)
    if not search_result:
        print("No search results found")
        return

    # Process each job
    for job in search_result.data.jobs.items:
        # Get job details
        job_detail = client.get_job_detail(job_id=job.id)
        if not job_detail:
            continue

        # Process the job
        job_manager.process_job(job.id, search_result, job_detail)

        # Add a small delay between applications
        time.sleep(1)

if __name__ == "__main__":
    main() 
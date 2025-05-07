from kariyer_client import KariyerSearch
from job_detail_client import JobDetailClient
from job_manager import JobManager
import time

def main():
    auth_token = "<auth_token>"
    member_id = "<member_id>"
    kariyer = KariyerSearch(auth_token)
    client = JobDetailClient(auth_token)
    job_manager = JobManager(auth_token)
    
    page = 1
    while True:
        print(f"\nProcessing page {page}")
        # Search for jobs
        search_result = kariyer.search(member_id=member_id, page=page, size=50,url="___wa=1,2,5,16,22,54,55,63,78___hc=N___dsaj=true")
        if not search_result:
            print("No search results found")
            break

        # Eğer sayfada hiç ilan yoksa döngüyü sonlandır
        if not search_result.data.jobs.items:
            print("No more jobs found")
            break

        # Daha önce işlenmiş ilanları filtrele
        filtered_jobs = [
            job for job in search_result.data.jobs.items 
            if str(job.id) not in job_manager.applied_jobs 
            and str(job.id) not in job_manager.failed_jobs
        ]

        if not filtered_jobs:
            print(f"No new jobs found on page {page}")
            page += 1
            continue

        print(f"Found {len(filtered_jobs)} new jobs on page {page}")

        # Process each job
        for job in filtered_jobs:
            # Get job details
            job_detail = client.get_job_detail(job_id=job.id)
            if not job_detail:
                continue

            # Process the job
            job_manager.process_job(job.id, search_result, job_detail)

            # Add a small delay between applications
            time.sleep(1)

        # Sayfa arası bekleme
        time.sleep(2)
        page += 1

if __name__ == "__main__":
    main() 
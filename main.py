from kariyer_client import KariyerSearch
from job_detail_client import JobDetailClient
from application_service import ApplicationService
from application_client import ApplicationClient
import json
import time
import os
from datetime import datetime

def load_job_set(filename: str) -> set:
    """İş ilanlarını dosyadan set olarak yükler."""
    if not os.path.exists(filename):
        return set()
    
    with open(filename, 'r') as f:
        return set(line.strip() for line in f)

def save_job_to_set(filename: str, job_id: int):
    """İş ilanını dosyaya set olarak kaydeder."""
    jobs = load_job_set(filename)
    jobs.add(str(job_id))
    with open(filename, 'w') as f:
        for job in sorted(jobs):
            f.write(f"{job}\n")

def save_error_log(job_id: int, error_message: str, error_text: str = None):
    """Hata detaylarını log dosyasına kaydeder."""
    # Eğer "daha önce başvuru yapıldı" hatası ise loglama
    if "Bu ilana daha önce başvuru yaptın" in error_message:
        return
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("failed_jobs_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Job ID: {job_id}\n")
        f.write(f"Error Message: {error_message}\n")
        if error_text:
            f.write(f"Error Details:\n{error_text}\n")
        f.write(f"{'='*50}\n")

def is_already_applied_error(error_text: str) -> bool:
    """Hata mesajının 'daha önce başvuru yapıldı' hatası olup olmadığını kontrol eder."""
    if not error_text:
        return False
    try:
        error_data = json.loads(error_text)
        error_message = error_data.get("body", {}).get("message", "")
        return "Bu ilana daha önce başvuru yaptın" in error_message
    except:
        return False

def main():
    auth_token = "<auth_token>"
    kariyer = KariyerSearch(auth_token)
    client = JobDetailClient(auth_token)
    application_service = ApplicationService()
    application_client = ApplicationClient(auth_token)
    
    # Başvurulan ve başarısız ilanları yükle
    applied_jobs_file = "applied_jobs.txt"
    failed_jobs_file = "failed_jobs.txt"
    applied_jobs = load_job_set(applied_jobs_file)
    failed_jobs = load_job_set(failed_jobs_file)
    
    # Search for jobs
    search_result = kariyer.search(member_id=26991322, size=50)
    if not search_result:
        print("No search results found")
        return

    # Process each job
    for job in search_result.data.jobs.items:
        # Eğer ilan daha önce başvurulmuşsa veya başarısız olmuşsa atla
        if str(job.id) in applied_jobs or str(job.id) in failed_jobs:
            print(f"Skipping job {job.id} - Already applied or failed")
            continue

        print(f"\nProcessing job {job.id}")
        
        # Get job details
        job_detail = client.get_job_detail(job_id=job.id)
        if not job_detail:
            print(f"Could not get details for job {job.id}")
            save_job_to_set(failed_jobs_file, job.id)
            save_error_log(job.id, "Could not get job details")
            continue

        # Create application body
        application_body = application_service.create_application_body(search_result, job_detail, job.id)
        if not application_body:
            print(f"Could not create application body for job {job.id}")
            save_job_to_set(failed_jobs_file, job.id)
            save_error_log(job.id, "Could not create application body")
            continue

        # Apply to the job
        print(f"Applying to job {job.id}")
        result = application_client.apply(application_body)
        
        if result:
            if result.get("header", {}).get("isSuccess", False):
                print(f"Successfully applied to job {job.id}")
                save_job_to_set(applied_jobs_file, job.id)
            else:
                error_message = result.get("body", {}).get("message", "")
                if "Bu ilana daha önce başvuru yaptın" in error_message:
                    print(f"Already applied to job {job.id}")
                    save_job_to_set(applied_jobs_file, job.id)
                else:
                    print(f"Failed to apply to job {job.id}")
                    print(f"Error: {error_message}")
                    save_job_to_set(failed_jobs_file, job.id)
                    save_error_log(job.id, error_message, json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Response text'ten hata mesajını kontrol et
            error_text = application_client.last_error_text
            if is_already_applied_error(error_text):
                print(f"Already applied to job {job.id}")
                save_job_to_set(applied_jobs_file, job.id)
            else:
                print(f"Failed to apply to job {job.id}")
                save_job_to_set(failed_jobs_file, job.id)
                save_error_log(job.id, "Request failed", error_text)

        # Add a small delay between applications
        time.sleep(1)

if __name__ == "__main__":
    main() 
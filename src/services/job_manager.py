import os
import json
from datetime import datetime
from typing import Set, Optional, Dict, Any
from src.models.job_detail_models import JobDetailResponse
from src.models.search_models import Response
from src.services.application_service import ApplicationService
from src.clients.application_client import ApplicationClient
from src.services.job_tracker import JobTracker

class JobManager:
    def __init__(self, auth_token: str):
        self.applied_jobs_file = "generated/applied_jobs.txt"
        self.failed_jobs_file = "generated/failed_jobs.txt"
        self.failed_jobs_log_file = "generated/failed_jobs_logs.txt"
        self.applied_jobs = self._load_job_set(self.applied_jobs_file)
        self.failed_jobs = self._load_job_set(self.failed_jobs_file)
        
        # Servisleri başlat
        self.application_service = ApplicationService()
        self.application_client = ApplicationClient(auth_token)
        self.job_tracker = JobTracker()

    def _load_job_set(self, filename: str) -> Set[str]:
        """İş ilanlarını dosyadan set olarak yükler."""
        if not os.path.exists(filename):
            return set()
        
        with open(filename, 'r') as f:
            return set(line.strip() for line in f)

    def save_job_to_set(self, filename: str, job_id: int):
        """İş ilanını dosyaya set olarak kaydeder."""
        jobs = self._load_job_set(filename)
        jobs.add(str(job_id))
        with open(filename, 'w') as f:
            for job in sorted(jobs):
                f.write(f"{job}\n")

    def save_error_log(self, job_id: int, error_message: str, error_text: str = None):
        """Hata detaylarını log dosyasına kaydeder."""
        # Eğer "daha önce başvuru yapıldı" hatası ise loglama
        if "Bu ilana daha önce başvuru yaptın" in error_message:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.failed_jobs_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Job ID: {job_id}\n")
            f.write(f"Error Message: {error_message}\n")
            if error_text:
                f.write(f"Error Details:\n{error_text}\n")
            f.write(f"{'='*50}\n")

    def is_already_applied_error(self, error_text: str) -> bool:
        """Hata mesajının 'daha önce başvuru yapıldı' hatası olup olmadığını kontrol eder."""
        if not error_text:
            return False
        try:
            error_data = json.loads(error_text)
            error_message = error_data.get("body", {}).get("message", "")
            return "Bu ilana daha önce başvuru yaptın" in error_message
        except:
            return False

    def is_job_processed(self, job_id: int) -> bool:
        """İş ilanının daha önce işlenip işlenmediğini kontrol eder."""
        return str(job_id) in self.applied_jobs or str(job_id) in self.failed_jobs

    def process_job(self, job_id: int, search_result: Response, job_detail: JobDetailResponse) -> bool:
        """İş ilanını işler ve başvuru yapar."""
        # Eğer ilan daha önce işlenmişse atla
        if str(job_id) in self.applied_jobs:
            print(f"Skipping job {job_id} - Already applied")
            return True
        elif str(job_id) in self.failed_jobs:
            print(f"Skipping job {job_id} - Previously failed")
            return False

        print(f"\nProcessing job {job_id}")

        # Search'ten iş ilanı bilgilerini al
        job = next((job for job in search_result.data.jobs.items if job.id == job_id), None)
        if not job:
            print(f"Job {job_id} not found in search results")
            return False

        # Application body oluştur
        application_body = self.application_service.create_application_body(search_result, job_detail, job_id)
        if not application_body:
            print(f"Failed to create application body for job {job_id}")
            self.save_job_to_set(self.failed_jobs_file, job_id)
            self.save_error_log(job_id, "Could not create application body")
            return False

        # Başvuru yap
        print(f"Applying to job {job_id}")
        result = self.application_client.apply(application_body)

        if result:
            if result.get("header", {}).get("isSuccess", False):
                print(f"Successfully applied to job {job_id}")
                self.save_job_to_set(self.applied_jobs_file, job_id)
                
                # Excel'e kaydet
                form_questions = []
                form_answers = []
                for form in job_detail.result.job_form:
                    for question in form.question_list:
                        form_questions.append({
                            "id": question.id,
                            "text": question.question
                        })
                        # Cevabı bul
                        answer = None
                        if form.answer:
                            answer = form.answer
                        else:
                            selected_choice = next(
                                (choice for choice in question.question_choices if choice.is_selected),
                                None
                            )
                            if selected_choice:
                                answer = selected_choice.choice
                            elif form.answered_choice_id:
                                matching_choice = next(
                                    (choice for choice in question.question_choices 
                                     if choice.id == form.answered_choice_id),
                                    None
                                )
                                if matching_choice:
                                    answer = matching_choice.choice
                        
                        form_answers.append({
                            "question_id": question.id,
                            "answer": answer
                        })
                
                self.job_tracker.add_application(
                    job_id=job_id,
                    company_name=job.company_name,
                    job_title=job.title,
                    form_questions=form_questions,
                    form_answers=form_answers
                )
                
                return True
            else:
                error_message = result.get("body", {}).get("message", "")
                if "Bu ilana daha önce başvuru yaptın" in error_message:
                    print(f"Already applied to job {job_id} (detected during application)")
                    self.save_job_to_set(self.applied_jobs_file, job_id)
                    return True
                else:
                    print(f"Failed to apply to job {job_id}")
                    print(f"Error: {error_message}")
                    self.save_job_to_set(self.failed_jobs_file, job_id)
                    self.save_error_log(job_id, error_message, json.dumps(result, indent=2, ensure_ascii=False))
                    return False
        else:
            # Response text'ten hata mesajını kontrol et
            error_text = self.application_client.last_error_text
            if self.is_already_applied_error(error_text):
                print(f"Already applied to job {job_id} (detected from error response)")
                self.save_job_to_set(self.applied_jobs_file, job_id)
                return True
            else:
                print(f"Failed to apply to job {job_id} (request failed)")
                self.save_job_to_set(self.failed_jobs_file, job_id)
                self.save_error_log(job_id, "Request failed", error_text)
                return False
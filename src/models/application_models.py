from typing import List, Dict, Any

class ApplicationBody:
    def __init__(self, resume_id: str, job_id: int, job_code: str, company_id: int):
        self.resume_id = resume_id
        self.job_id = job_id
        self.job_code = job_code
        self.company_id = company_id
        self.cover_letter_id = 0
        self.is_qualification_notified = False
        self.city_answer = []
        self.form_question_answer_dtos = []
        self.job_application_type = 1
        self.is_job_apply_save_candidate_control = True

    def add_city_answer(self, order: int, value: str):
        """Şehir cevabı ekler."""
        self.city_answer.append({
            "order": order,
            "value": value
        })

    def add_form_question_answer(self, key: str, value: str):
        """Form sorusu cevabı ekler."""
        self.form_question_answer_dtos.append({
            "key": key,
            "value": value
        })

    def to_dict(self) -> Dict[str, Any]:
        """Application body'yi dictionary formatına çevirir."""
        return {
            "ResumeId": self.resume_id,
            "JobId": self.job_id,
            "JobCode": self.job_code,
            "CompanyId": self.company_id,
            "CoverLetterId": self.cover_letter_id,
            "IsQualificationNotified": self.is_qualification_notified,
            "CityAnswer": self.city_answer,
            "FormQuestionAnswerDtos": self.form_question_answer_dtos,
            "JobApplicationType": self.job_application_type,
            "IsJobApplySaveCandidateControl": self.is_job_apply_save_candidate_control
        } 
import logging
from typing import Optional, List, Tuple
from job_detail_models import JobDetailResponse
from search_models import Response
from application_models import ApplicationBody

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApplicationService:
    def __init__(self):
        self.priority_cities = ["34", "82", "99"]  # Avrupa, Asya, farketmez

    def _get_city_answers(self, job_detail: JobDetailResponse) -> List[Tuple[int, str]]:
        """Şehir cevaplarını öncelik sırasına göre döndürür."""
        cities = []
        for location in job_detail.result.job_location:
            # is_location_selected kontrolünü kaldırdık
            if location.city_id:  # Sadece city_id varsa ekle
                order = location.selected_location_order or 1  # Eğer order yoksa 1 olarak al
                cities.append((order, str(location.city_id)))
        
        # Eğer hiç şehir bulunamadıysa, öncelikli şehirleri ekle
        if not cities:
            for i, city_id in enumerate(self.priority_cities, 1):
                cities.append((i, city_id))
        
        # Öncelik sırasına göre sırala
        cities.sort(key=lambda x: x[0])
        return cities

    def _get_form_answers(self, job_detail: JobDetailResponse) -> List[Tuple[str, str]]:
        """Form sorularının cevaplarını döndürür."""
        answers = []
        for form in job_detail.result.job_form:
            for question in form.question_list:
                # Önce answer field'ını kontrol et
                if form.answer:
                    answers.append((str(question.id), form.answer))
                    continue

                # Sonra isSelected true olan choice'ı kontrol et
                selected_choice = next(
                    (choice for choice in question.question_choices if choice.is_selected),
                    None
                )
                if selected_choice:
                    answers.append((str(question.id), str(selected_choice.id)))
                    continue

                # Son olarak answeredChoiceId'yi kontrol et
                if form.answered_choice_id:
                    matching_choice = next(
                        (choice for choice in question.question_choices 
                         if choice.id == form.answered_choice_id),
                        None
                    )
                    if matching_choice:
                        answers.append((str(question.id), str(matching_choice.id)))
                        continue

                # Hiçbir cevap bulunamadıysa log'a kaydet
                logger.warning(f"No answer found for question {question.id} in job {job_detail.result.job_form[0].job_id}")

        return answers

    def create_application_body(self, search_result: Response, job_detail: JobDetailResponse, job_id: int) -> Optional[ApplicationBody]:
        """Search ve detail verilerinden application body oluşturur."""
        try:
            # Search'ten doğru iş ilanını bul
            job = next((job for job in search_result.data.jobs.items if job.id == job_id), None)
            if not job:
                logger.error(f"Job with id {job_id} not found in search results")
                return None

            resume_id = job_detail.result.resume_list[0].encrypted_id

            # Application body oluştur
            body = ApplicationBody(
                resume_id=resume_id,
                job_id=job.id,
                job_code=job.job_code,
                company_id=job.company_id
            )

            # Şehir cevaplarını ekle
            city_answers = self._get_city_answers(job_detail)
            for order, city_id in city_answers:
                body.add_city_answer(order, city_id)

            # Form cevaplarını ekle
            form_answers = self._get_form_answers(job_detail)
            for key, value in form_answers:
                body.add_form_question_answer(key, value)

            return body

        except Exception as e:
            logger.error(f"Error creating application body: {e}")
            return None 
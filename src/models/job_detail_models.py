from typing import List, Optional, Any

class QuestionChoice:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.posting_user = data.get('postingUser')
        self.form_id = data.get('formId')
        self.question_id = data.get('questionId')
        self.choice = data.get('choice')
        self.choice_order = data.get('choiceOrder')
        self.point = data.get('point')
        self.is_selected = data.get('isSelected')

class QuestionProperty:
    def __init__(self, data: dict):
        self.question_id = data.get('questionId')
        self.property_name = data.get('propertyName')
        self.value = data.get('value')

class QuestionList:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.form_id = data.get('formId')
        self.posting_user = data.get('postingUser')
        self.question_type = data.get('questionType')
        self.question = data.get('question')
        self.mandatory = data.get('mandatory')
        self.time = data.get('time')
        self.question_order = data.get('questionOrder')
        self.choice_count = data.get('choiceCount')
        self.question_choices = [QuestionChoice(choice) for choice in data.get('questionChoices', [])]
        self.question_properties = [QuestionProperty(prop) for prop in data.get('questionProperties', [])]

class JobForm:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.posting_user = data.get('postingUser')
        self.job_id = data.get('jobId')
        self.form_id = data.get('formId')
        self.mandatory = data.get('mandatory')
        self.form_name = data.get('formName')
        self.question_list = [QuestionList(q) for q in data.get('questionList', [])]
        self.haskipped_question = data.get('haskippedQuestion')
        self.has_time_question = data.get('hasTimeQuestion')
        self.answered_choice_id = data.get('answeredChoiceId')
        self.is_standart = data.get('isStandart')
        self.answer = data.get('answer')

class JobLocation:
    def __init__(self, data: dict):
        self.job_id = data.get('jobId')
        self.city_id = data.get('cityId')
        self.country_id = data.get('countryId')
        self.district_id = data.get('districtId')
        self.city_name = data.get('cityName')
        self.is_location_selected = data.get('isLocationSelected')
        self.selected_location_order = data.get('selectedLocationOrder')

class ResumeList:
    def __init__(self, data: dict):
        self.encrypted_id = data.get('encryptedId')
        self.resume_name = data.get('resumeName')
        self.is_selected = data.get('isSelected')

class Result:
    def __init__(self, data: dict):
        self.resume_list = [ResumeList(resume) for resume in data.get('resumeList', [])]
        self.cover_letter_list = data.get('coverLetterList', [])
        self.job_form = [JobForm(form) for form in data.get('jobForm', [])]
        self.job_location = [JobLocation(loc) for loc in data.get('jobLocation', [])]
        self.is_embargoed_any_companies = data.get('isEmbargoedAnyCompanies')
        self.is_group_companies = data.get('isGroupCompanies')
        self.approved_candidate = data.get('approvedCandidate')

class JobDetailResponse:
    def __init__(self, data: dict):
        self.version = data.get('version')
        self.status_code = data.get('statusCode')
        self.result = Result(data.get('result', {})) 
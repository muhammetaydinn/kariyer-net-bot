from typing import List, Optional

class Item:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.title = data.get('title')
        self.company_name = data.get('companyName')
        self.job_url = data.get('jobUrl')
        self.company_url = data.get('companyUrl')
        self.company_id = data.get('companyId')
        self.profile_id = data.get('profileId')
        self.position_level = data.get('positionLevel')
        self.work_model = data.get('workModel')
        self.is_easy_apply = data.get('isEasyApply')
        self.job_code = data.get('jobCode')
        self.position_id = data.get('positionId')

class Jobs:
    def __init__(self, data: dict):
        self.items = [Item(item) for item in data.get('items', [])]
        self.current_page = data.get('currentPage')

class Data:
    def __init__(self, data: dict):
        self.jobs = Jobs(data.get('jobs', {}))
        self.search_url = data.get('searchUrl')
        self.is_searched = data.get('isSearched')
        self.current_page = data.get('currentPage')

class Response:
    def __init__(self, data: dict):
        self.status_code = data.get('statusCode')
        self.status = data.get('status')
        self.data = Data(data.get('data', {}))
        self.message = data.get('message')
        self.error = data.get('error') 
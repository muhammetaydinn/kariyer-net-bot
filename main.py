from kariyer_client import KariyerSearch
from job_detail_client import JobDetailClient

def main():
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImUyZDMyMTc4ZWExMDk1ODYyMmIyMzI0NmI2OTI3Yjk3IiwidHlwIjoiSldUIn0.eyJuYmYiOjE3NDY2MjQ3MTIsImV4cCI6MTc0NjYyODMxMiwiaXNzIjoiaHR0cDovL3Rva2VuLmthcml5ZXIubmV0IiwiTG9naW5JZCI6IjI2OTkxMzIyIiwiQ2xpZW50VHlwZSI6IkNhbmRpZGF0ZSIsImNsaWVudF9pZCI6IktuZXRfQ2FuZGlkYXRlX0NsaWVudF9JZCIsImF1ZCI6WyJodHRwOi8vdG9rZW4ua2FyaXllci5uZXQvcmVzb3VyY2VzIiwiS25ldF9TY29wZV9BcGlfMSJdLCJzY29wZSI6WyJLbmV0X1Njb3BlX0FwaV8xIl19.cynkF7M5ZWGc9rO99T6acI-L55vY0V-MnbLUKlNcc9lNS97vk89raoCn8349Hi_XMgaxwEm0huV6W6HVGigL9pKYIAr2lt09jxZFdJ7lYbwqKMbKhPJZDLgqwyeXLGMPN7SZ9h2ZYxLtUA1EzW4lGQcBSnvtbWEa7ZZnZjQCJ0LVXE-ncwinNOmyGkvNH_4JTl5XrQJTV01f1QBKi5Ao6lyUZ3ypejs-YtK9gYjV4GyOE-1PS3Z0RsoSZacEzvUxTyF_MGERx9mgc73dcoA0ctqgNs_ruq1jClxw3hGjzRxkZ83twyZgUp_WUTwLayNh3-aAb0GrWFa0CEu0AAiryw"
    kariyer = KariyerSearch(auth_token)
    client = JobDetailClient(auth_token)
    
    result = kariyer.search(member_id=26991322)
    if result:
        for job in result.data.jobs.items:
            print(vars(job))

    result = client.get_job_detail(job_id=result.data.jobs.items[0].id)
    if result:
        print(vars(result.result))

if __name__ == "__main__":
    main() 
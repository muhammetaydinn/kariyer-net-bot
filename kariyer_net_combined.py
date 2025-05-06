import requests
from time import sleep

member_id = "<YOUR-MEMBER-ID-AS-INTEGER>"  # Member ID (replace with actual member ID) ex: 269987654
url_filter = ("YOUR-FILTER-KEYWORD")
token = "<YOUR-BEARER-TOKEN>"  # Bearer token (replace with your token)
x_hash = "<YOUR-X-HASH>"  # X-Hash value (replace with actual hash value if needed)
resume_id = "<YOUR-RESUME-ID>"  # Resume ID (replace with actual resume ID)
current_page = 1  # Page number to retrieve
page_size = 50  # Number of results per page


def job_search(
    member_id,
    url_filter,
    token,
    x_hash,
    current_page=1,
    page_size=50,
):
    url = "https://candidatesearchapigateway.kariyer.net/search"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "tr-TR",
        "Authorization": f"Bearer {token}",
        "ClientType": "1",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.kariyer.net",
        "Referer": "https://www.kariyer.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Hash": x_hash,  # Replace with actual hash value if needed
    }

    # Search params adjusted to match the structure from the curl command
    data = {
        "memberId": member_id,  # Dynamic member ID
        "currentPage": current_page,
        "size": page_size,  # Dynamic page size
        "url": url_filter,  # Dynamic filter keyword
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        jobs = response.json()
        job_details = [
            {
                "id": job["id"],
                "jobCode": job["jobCode"],
                "companyId": job["companyId"],
            }
            for job in jobs.get("data", {}).get("jobs", {}).get("items", [])
        ]
        print(f"Found {len(job_details)} jobs.")
        return job_details
    else:
        print(f"Error: {response.status_code}")
        return []


def apply_job(
    job_id,
    resume_id,
    job_code,
    company_id,
    token,
    city_answer=None,
    form_question_answer_dtos=None,
):
    url = "https://candidatewebapigw.kariyer.net/jobapplications"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "tr-TR",
        "ApplicationVersion": "v1.0",
        "Authorization": f"Bearer {token}",
        "ClientType": "1",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.kariyer.net",
        "Referer": "https://www.kariyer.net/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "JobId": job_id,
        "ResumeId": resume_id,
        "IsQualificationNotified": True,
        "JobApplicationType": 2,
        "IsJobApplySaveCandidateControl": True,
        "CityAnswer": city_answer if city_answer else [],
        "FormQuestionAnswerDtos": (
            form_question_answer_dtos if form_question_answer_dtos else []
        ),
        "JobCode": job_code,
        "CompanyId": company_id,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Job application submitted successfully.")
        return response.json()
    else:
        try:
            error_message = response.json()["body"]["message"]
        except (KeyError, ValueError):
            error_message = f"Status code: {response.status_code}, Response: {response.text}"
        print(f"Failed to apply for the job: {error_message}")
        return error_message


def main():
    applied_jobs = set()
    try:
        with open("applied_jobs.txt", "r") as f:
            for line in f:
                applied_jobs.add(line.strip())
        current_page = 1
        while True:
            # Job search
            job_details = job_search(
                member_id, url_filter, token, x_hash, current_page, page_size
            )
            if not job_details:
                print("No more jobs found. Exiting.")
                break

            print(f"Found {len(job_details)} job IDs on page {current_page}.")
            for job in job_details:
                job_id = job['id']
                if str(job_id) in applied_jobs:
                    print(f"Skipping Job ID: {job_id} (already applied)")
                    continue

                print(f"applying Job ID: {job_id}")
                result = apply_job(
                    job_id,
                    resume_id,
                    job["jobCode"],
                    job["companyId"],
                    token,
                )
                applied_jobs.add(str(job_id))
                sleep(1)  # Sleep for 1 second between applications to avoid rate limiting

            current_page += 1

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        with open("applied_jobs.txt", "w") as f:
            for job_id in applied_jobs:
                f.write(str(job_id) + "\n")


if __name__ == "__main__":
    main()

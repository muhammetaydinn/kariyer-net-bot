from src.utils.job_searcher import JobSearcher

def main():
    auth_token = "<auth_token>"
    member_id = 00000000 # member id
    searcher = JobSearcher(auth_token, member_id)
    searcher.search_and_process_jobs()

if __name__ == "__main__":
    main() 
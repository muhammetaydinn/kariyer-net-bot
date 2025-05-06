# Kariyer.net Job Application Bot

This script automates the job application process on Kariyer.net. It searches for jobs based on your criteria and automatically applies to them.

## Prerequisites

* Python 3.6 or higher
* `requests` package: `pip install requests`
* A Kariyer.net account

## Setup

1. **Install Dependencies:**

    ```bash
    pip install requests
    ```

2. **Obtain Credentials:**

    * Log in to your Kariyer.net account.
    * Go to the job search page and define your search criteria (e.g., keywords, location, etc.).
    * Open the browser's developer tools (usually by pressing F12).
    * **Find `member_id`, `token`, and `x_hash`:**
        * Go to the "Network" tab in the developer tools.
        * Perform a job search on the website.
        * Look for a request to `candidatesearchapigateway.kariyer.net/search`.
        * Inspect the request headers to find the `Authorization` header (which contains the `token`) and the `X-Hash` header.
        * The `member_id` is usually part of the request payload.
    * **Find `url_filter`:**
        * In the same `candidatesearchapigateway.kariyer.net/search` request, find the request payload (the data being sent in the request).
        * The `url` field in the payload is your `url_filter`.
    * **Find `resume_id`:**
        * Open a job posting and start the application process (you don't need to actually submit the application).
        * Look for a request to `candidatewebapigw.kariyer.net/jobapplications`.
        * Inspect the request payload to find the `ResumeId` field.

3. **Configure the Script:**

    * Open the `kariyer_net_combined.py` file in a text editor.
    * Replace the placeholder values for `member_id`, `url_filter`, `token`, `x_hash`, and `resume_id` with your actual values.

        ```python
        member_id = 12365498  # Member ID (replace with actual member ID)
        url_filter = "YOUR-URL-FILTER"  # some criterias of saerch
        token = "YOUR_TOKEN"  # Bearer token (replace with your token)
        x_hash = "YOUR_X_HASH"  # X-Hash value (replace with actual hash value if needed)
        resume_id = "YOUR_RESUME_ID"  # Resume ID (replace with actual resume ID)
        ```

    * **Important:** Do not commit the `kariyer_net_combined.py` file to a public repository, as it contains your sensitive credentials.

## Usage

1. **Run the Script:**

    ```bash
    python kariyer_net_combined.py
    ```

2. **Monitor the Output:**

    The script will print the following information:

    * The number of jobs found.
    * The job IDs being applied to.
    * Success or failure messages for each job application.
    * Any errors encountered.

3. **Applied Jobs:**

    The script will create a file named `applied_jobs.txt` in the same directory. This file contains a list of all the job IDs that the script has attempted to apply to. The script will skip any job IDs that are already in this file.

## Notes

* The script pauses for 1 second between each job application to avoid rate limiting.
* The `token` is valid for a limited time (usually 1 hour). You will need to obtain a new token when the old one expires.
* The `url_filter` is specific to your search criteria. If you change your search criteria, you will need to update the `url_filter` accordingly.

## Disclaimer

This script is provided as-is, without any warranty. Use it at your own risk. The author is not responsible for any consequences of using this script, including but not limited to account suspension or termination.

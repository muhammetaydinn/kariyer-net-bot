import pandas as pd
from datetime import datetime
from typing import Dict, Any, List

class JobTracker:
    def __init__(self, excel_file: str = "applied_job_data.xlsx"):
        self.excel_file = excel_file
        self._initialize_excel()

    def _initialize_excel(self):
        """Initialize Excel file with headers if it doesn't exist."""
        try:
            # Try to read existing file
            pd.read_excel(self.excel_file)
        except FileNotFoundError:
            # Create new file with headers
            df = pd.DataFrame(columns=[
                'Job ID',
                'Company Name',
                'Job Title',
                'Application Date',
                'Form Questions',
                'Form Answers'
            ])
            df.to_excel(self.excel_file, index=False)

    def add_application(self, job_id: int, company_name: str, job_title: str, 
                       form_questions: List[Dict[str, str]], form_answers: List[Dict[str, str]]):
        """Add a new job application to the Excel file."""
        try:
            # Read existing data
            df = pd.read_excel(self.excel_file)
            
            # Create new row
            new_row = {
                'Job ID': job_id,
                'Company Name': company_name,
                'Job Title': job_title,
                'Application Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Form Questions': str(form_questions),
                'Form Answers': str(form_answers)
            }
            
            # Append new row
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save to Excel
            df.to_excel(self.excel_file, index=False)
            
        except Exception as e:
            print(f"Error adding application to Excel: {e}") 
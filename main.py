from jobs_notify import JobNotifier
import dotenv
import os

dotenv.load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
PASSWORD = os.getenv("PASSWORD")

if __name__ == "__main__":
    URL = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=Data+analyst&txtLocation="

    find_jobs = JobNotifier(URL, FROM_EMAIL, TO_EMAIL, PASSWORD)
    find_jobs.run()
    



    
                




    

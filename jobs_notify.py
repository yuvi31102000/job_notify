import requests
from bs4 import BeautifulSoup
import smtplib

class JobNotifier:
    """A class to scrape job listings from TimesJobs and send job alerts via email. """

    def __init__(self, url, from_email, to_email, password):
        """
        Initialize the JobNotifier with URL and email credentials.
        
        Args:
            url (str): The URL to scrape jobs from.
            from_email (str): The sender email address.
            to_email (str): The recipient email address.
            password (str): The password or app password for the sender email.
        """
        self.url = url 
        self.jobs = []
        self.from_email = from_email
        self.to_email = to_email
        self.password = password


    def fetch_jobs(self) -> list:
        """
        This method sends a GET request to the specified URL, parses the HTML content,
        and extracts job postings using BeautifulSoup.
        
        Returns:
            list: A list of BeautifulSoup elements representing job postings.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            self.jobs = soup.find_all(name='li', class_='clearfix job-bx wht-shd-bx')
        else:
            print(f"Failed to retrieve jobs. Status code: {response.status_code}")
        return self.jobs


    def is_job_recent(self, job) -> bool:
        """
        Checks whether the job post is recent (i.e., posted a few days ago).
        This method looks for the 'sim-posted' span in the job posting HTML to determine recency.

        Args:
            job (bs4.element.Tag): The job posting HTML element.
        Returns:
            bool: True if the job was posted recently, False otherwise.
        """
        job_posted_date = job.find(name='span', class_='sim-posted')
        return job_posted_date.text.strip() and 'few' in job_posted_date.text.lower()


    def extract_job_details(self, job) -> dict:
        """ 
        Extracts relevant details from a job posting.
        This includes the job title, company name, skills required, and job link.
        Args:
            job (bs4.element.Tag): The job posting HTML element.
        Returns:
            dict: A dictionary containing job title, company name, skills list, and job link. 
        """
        job_title = job.find(name='h2')
        company_name = job.find(name=['div', 'h3'], class_= 'joblist-comp-name')
        job_link = job.header.h2.a
        skills = job.find(name=['div', 'span'], class_='srp-skills')
        if skills:
            skill_list = [skill.strip().lower() for skill in skills.text.split('\n') if skill.strip()]
            skills =  ', '.join(skill_list)
        else:
            print("Skills: Not found")
        
        return {
                'title': job_title.text.strip(),
                'company': company_name.text.strip(),
                'skills': skill_list,
                'link': job_link['href']
            }


    def send_email_notification(self, all_jobs) -> None:
        """
        This method connects to the SMTP server, constructs the email body with job details,
        and sends the email to the specified recipient.

        Args:
            all_jobs (list): List of dictionaries, each containing details of one job.
        """
        try:
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(user=self.from_email, password=self.password)

            subject = "Data Analyst Job Alerts from TimesJobs!"

            html_body = """
            <html>
                <body style="font-family: Calibri, sans-serif; background-color: #f1f5f9; padding: 20px;">
                    <div style="max-width: 650px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color:#1a73e8; text-align: center;">📊 Data Analyst Job Opportunities</h2>
                        <p style="color: #333333; font-size: 15px;">Hello 👋, here are the latest data analyst job openings curated just for you:</p>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;"/>
            """

            for job in all_jobs:
                html_body += f"""
                    <div style="background-color: #f9fafb; padding: 20px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
                        <h3 style="margin: 0 0 10px 0; color: #0d47a1; font-weight: bold;">{job['title']}</h3>
                        <p style="margin: 5px 0;">{job['company']}</p>
                        <p style="margin: 5px 0;"><strong>Skills:<strong>{', '.join(job['skills'])}</p>
                        <p style="margin: 5px 0;"><a href="{job['link']}" style="color: #1a73e8;" target="_blank">Apply Now</a></p>
                    </div>
                """

            html_body += """
                        <p style="font-size: 12px; color: #6b7280; text-align: center; margin-top: 30px;">
                            This is an automated notification from your TimesJobs Notifier.<br>
                            Stay curious. Keep growing! 🚀
                        </p>
                    </div>
                </body>
            </html>
            """

            message = f"Subject: {subject}\nMIME-Version: 1.0\nContent-Type: text/html\n\n{html_body}"

            connection.sendmail(
                from_addr=self.from_email,
                to_addrs=self.to_email,
                msg=message.encode('utf-8')
            )
            connection.close()
            print("✅ Email sent successfully!")

        except smtplib.SMTPConnectError:
            print("Failed to connect to the email server. Check your internet connection or email server settings.")
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate. Check your email and password.")
        except requests.RequestException as e:
            print(f"Request error occurred: {e}")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")


    def run(self) -> None:
        """ 
        The main method to run the job notifier. It fetches jobs, checks for recent postings,
        extracts job details, and sends an email notification if there are recent jobs.
        """
        jobs = self.fetch_jobs()
        all_jobs = []
        for job in jobs:
            if self.is_job_recent(job):
                job_details = self.extract_job_details(job)
                all_jobs.append(job_details)
        if all_jobs:
            self.send_email_notification(all_jobs)
        else:
            print("No recent jobs found.")
            



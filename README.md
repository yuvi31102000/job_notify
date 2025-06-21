# Job Notify

Job Notify is a Python project that automates the process of finding recent Data Analyst job postings from TimesJobs.com and sending them via email. It scrapes job listings, filters recently posted jobs, and delivers a formatted HTML email containing job information to the recipient.

---

## Features

- Scrapes job listings from TimesJobs.com
- Filters only recently posted jobs (e.g., posted "a few days ago")
- Extracts job title, company name, required skills, and job link
- Sends job alerts via email in a clean HTML format
- Uses environment variables to manage sensitive email credentials securely

---

## Technologies Used

- Python 3
- BeautifulSoup (for web scraping)
- Requests (for HTTP requests)
- smtplib (for sending emails via SMTP)
- python-dotenv (for environment variable management)

---


---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yuvi31102000/job_notify.git
cd job_notify




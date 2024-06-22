import requests
from bs4 import BeautifulSoup
import urllib3
from .models import Jobs

def InfoPark():
    # Suppress the warning for unverified HTTPS requests
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Specify the URL of the website you want to scrape
    website_url = "https://infopark.in/ml/companies/job-search"
    # Send a GET request to the website
    res = requests.get(website_url, verify=False)
    res.raise_for_status()  # Raise an error if the request was unsuccessful

    soup = BeautifulSoup(res.text, 'lxml')
    jobs = soup.find_all("div", {"class":"row company-list joblist"})[:20]
    for job in jobs:
        title_element = job.find("a")
        title = title_element.text
        link = title_element["href"]
        company_name = job.find("div",{"class":"jobs-comp-name"}).text
        last_date = job.find("div", {"class":"job-date"}).text
        Jobs(
            title = title,
            company= company_name,
            location= "ernakulam",
            link= link,
            provider="infopark"
        ).save()
        #print(title,company_name,link,last_date)
    print(len(jobs))
    

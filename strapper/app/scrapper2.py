# web scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# html parsing
from bs4 import BeautifulSoup

# dataframes
import pandas as pd

# async
import asyncio

# terminal formatting
from rich.progress import track
from rich.console import Console
from rich.table import Table

# instantiate global variables
df = pd.DataFrame(columns=["Title", "Location", "Company", "Link", "Description"])
console = Console()
table = Table(show_header=True, header_style="bold")

jobs=[]


async def scrapeJobDescription(url):
    global df
    driver = DriverOptions()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        jobDescription = soup.find(
            "div", class_="show-more-less-html__markup"
        ).text.strip()
        return jobDescription
    except:
        return ""


import traceback

def DriverOptions():
    chrome_driver_path = '/usr/bin/google-chrome'
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options)

    return driver

from itertools import islice
    

async def scrapeLinkedin(job,location):
    print("called")
    driver = DriverOptions()
    counter = 0
    pageCounter = 1
    job_data_list = []  # Create an empty list to store scraped job data

    while True:
        try:
            driver.get(
                f"https://www.linkedin.com/jobs/search/?&keywords={job}&location={location}&refresh=true&start={counter}"
            )

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            ulElement = soup.find("ul", class_="jobs-search__results-list")
            liElements = ulElement.find_all("li")
            if liElements != None:
                for item in track(liElements[:10], description=f"Linkedin - Page: {pageCounter}"):

                    print("fetching job")
                    jobTitle = item.find(
                        "h3", class_="base-search-card__title"
                    ).text.strip()
                    jobLocation = item.find(
                        "span", class_="job-search-card__location"
                    ).text.strip()
                    jobCompany = item.find(
                        "h4", class_="base-search-card__subtitle"
                    ).text.strip()
                    jobLink = item.find_all("a")[0]["href"]
                    jobImg = None
                    if "src" in item.find("img"):
                        jobImg = item.find("img")["src"]
                    else:
                        print("no image found")
                    jobDescription = await scrapeJobDescription(jobLink)

                    # Create a dictionary for each job
                    job_data = {
                        'title': jobTitle,
                        'location': jobLocation,
                        'company': jobCompany,
                        'link': jobLink,
                        'description': jobDescription,
                        'image': jobImg,
                    }

                    # Append job data to the list
                    job_data_list.append(job_data)

            continueInput = "n"

            if continueInput == "n":
                break

            counter += 25
            pageCounter += 1

        except Exception as e:
            print(traceback.format_exc())
            break

    driver.quit()
    
    return job_data_list

    


async def main(job,location):
    # get user input
    print(job,location)
    jobs=await scrapeLinkedin(job,location)
    # create table
    table.add_column("Title")
    table.add_column("Company")
    table.add_column("Location")
    table.add_column("Link")
    table.add_column("Description")
    # loop over dataframe and print rich table
    for index, row in df.iterrows():
        table.add_row(
            f"{row['Title']}",
            f"{row['Company']}",
            f"{row['Location']}",
            f"{row['Link']}",
            f"{(row['Description'])[:20]}...",
        )

    continueInput = "n"

    if continueInput == "y":
        df.to_csv(f"{inputJobTitle}_{inputJobLocation}_jobs.csv", index=False)
    
    return jobs
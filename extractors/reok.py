from requests import get
from bs4 import BeautifulSoup


def extract_reok_jobs(keyword):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = get(f"https://remoteok.com/remote-{keyword}-jobs",
                   headers=headers)

    if response.status_code != 200:
        print("Can't request website")

    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")
        for job_section in jobs:
            anchor = job_section.select_one("td a")
            position = job_section.find("h2", itemprop="title")
            company = job_section.find("h3", itemprop="name")
            location = job_section.find("div", class_="location")
            link = anchor['href']
            job_data = {
                "position": position.string.strip().replace(",", " "),
                "company": company.string.strip().replace(",", " "),
                "location": location.string.replace(",", " "),
                'link': f"https://remoteok.com/{link}"
            }
            results.append(job_data)
        return results

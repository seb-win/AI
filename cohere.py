import requests
import json
from bs4 import BeautifulSoup
from datetime import date
import support_functions

def main():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://jobs.lever.co/cohere/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }


    response = requests.get('https://jobs.lever.co/cohere/', headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    all = soup.find_all("div", {"class": "posting"})

    job = all[0]

    def get_details(job):
        span_tags = job.find_all('span')
        for span in span_tags:
            if span.has_attr('class') and 'location' in span['class']:
                location = span.text
            else:
                location = None
            if span.has_attr('class') and 'department' in span['class']:
                department = span.text
            else:
                department = None
            if span.has_attr('class') and 'commitment' in span['class']:
                commitment = span.text
            else:
                commitment = None
            if span.has_attr('class') and 'workplaceTypes' in span['class']:
                workplace = span.text
            else:
                workplace = None
        details = [location, department, commitment, workplace]
        return details

    jobs = []
    for job in all:
        try:
            jobTitle = job.find("h5").text
        except:
            jobTitle = None

        try:
            country = None
        except:
            country = None

        try:
            info = get_details(job)
            location = info[0]
        except:
            location = None

        try:
            commitment = info[2]
        except:
            commitment = None

        try:
            workplaceType = info[3]
        except:
            workplaceType = None

        try:
            id = job.find('a')['href'].split('id=')[1]
        except:
            id = None

        try:
            link = job.find("a").get("href")
        except:
            link = None

        try:
            response = requests.get(link)
            divs = BeautifulSoup(response.text, 'html.parser').find_all('div', class_='section page-centered')
            description = ''.join(div.get_text() for div in divs)
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            team = info[1]
        except:
            team = None

        job_details = {'jobTitle': jobTitle,
                            'country': country, 
                        'location': location, 
                            'commitment': commitment,
                        'workplaceType': workplaceType, 
                        'description': description, 
                        'id': id,
                        'createdAt': createdAt,
                        'link': link,
                        'team': team}
        jobs.append(job_details)

    cohere_dict = support_functions.create_dict('cohere', jobs)

    return cohere_dict

if __name__ == "__main__":
    main()






    



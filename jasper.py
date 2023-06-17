import requests
from bs4 import BeautifulSoup
from datetime import date
import support_functions

def main():
    headers = {
        'authority': 'boards.greenhouse.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get('https://boards.greenhouse.io/jasper23',  headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    all = soup.find_all('div', {'class': 'opening'})

    jobs = []
    for job in all:
        try:
            jobTitle = job.find('a').text
        except:
            jobTitle = None

        try:
            country = None
        except:
            country = None

        try:
            location = job.find('span', {'class': 'location'}).text
        except:
            location = None

        try:
            commitment = None
        except:
            commitment = None

        try:
            workplaceType = None
        except:
            workplaceType = None

        try:
            id = None
        except:
            id = None

        try:
            link = f"https://boards.greenhouse.io{job.find('a')['href']}"
        except:
            link = None

        try:
            desc_html = requests.get(link, headers=headers)
            desc_str = BeautifulSoup(desc_html.text, 'html.parser').find('div', {'id': 'content'}).get_text()
            description = support_functions.remove(desc_str)
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            team = soup.find('h3', {'id': job['department_id']}).text
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

    jasper_dict = support_functions.create_dict('jasper', jobs)

    return jasper_dict

if __name__ == "__main__":
    main()




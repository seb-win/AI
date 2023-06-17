import requests
from bs4 import BeautifulSoup
from datetime import date
import support_functions

def main():
    headers = {
        'authority': 'boards.eu.greenhouse.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://stability.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'for': 'stabilityai',
        'token': None,
        'b': 'https://stability.ai/careers',
    }

    response = requests.get('https://boards.eu.greenhouse.io/embed/job_board', params=params, headers=headers)

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
            id = job.find('a')['href'].split('id=')[1]
        except:
            id = None

        try:
            params['token'] = str(id)
            desc_html = requests.get('https://boards.eu.greenhouse.io/embed/job_app', params=params, headers=headers)
            desc_str = BeautifulSoup(desc_html.text, 'html.parser').find('div', {'id': 'content'}).get_text()
            description = support_functions.remove(desc_str)
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            link = job['absolute_url']
        except:
            link = None

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

    stability_dict = support_functions.create_dict('stability', jobs)

    return stability_dict

if __name__ == "__main__":
    main()



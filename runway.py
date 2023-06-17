import requests
import json
import support_functions
from bs4 import BeautifulSoup

def main():
    headers = {
        'authority': 'boards-api.greenhouse.io',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://runwayml.com',
        'referer': 'https://runwayml.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    params = {
        'content': 'true',
    }

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/runwayml/jobs', params=params, headers=headers)

    json_obj = json.loads(response.text)

    all = json_obj['jobs']

    jobs = []
    for job in all:
        try:
            jobTitle = job['title']
        except:
            jobTitle = None

        try:
            country = None
        except:
            country = None

        try:
            location = job['location']['name']
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
            id = job['id']
        except:
            id = None

        try:
            link = job['absolute_url']
        except:
            link = None

        try:
            params['token'] = str(id)
            desc_html = requests.get(link, headers=headers)
            desc_str = soup_desc = BeautifulSoup(desc_html.text, 'html.parser').find('div', {'id': 'content'}).get_text()
            description = support_functions.remove(desc_str)
        except:
            description = None

        try:
            createdAt = job['updated_at']
        except:
            createdAt = None

        try:
            team = job['departments'][0]['name']
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

    runway_dict = support_functions.create_dict('runway', jobs)

    return runway_dict

if __name__ == "__main__":
    main()





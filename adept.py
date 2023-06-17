import requests
import json
import html
from bs4 import BeautifulSoup
import support_functions

def main():
    headers = {
        'authority': 'boards-api.greenhouse.io',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.adept.ai',
        'referer': 'https://www.adept.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'content': 'true',
    }

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/adept/jobs', params=params, headers=headers)

    json_obj = json.loads(response.text)

    all = json_obj['jobs']


    jobs = []
    for job in all:
        try:
            jobTitle = job['title']
        except KeyError:
            jobTitle = None

        try:
            country = job['location']['name']
        except KeyError:
            country = None

        try:
            location = job['location']['name']
        except KeyError:
            location = None

        try:
            commitment = None
        except KeyError:
            commitment = None

        try:
            workplaceType = None
        except KeyError:
            workplaceType = None

        try:
            description = support_functions.remove(BeautifulSoup(html.unescape(job['content']), 'html.parser').get_text())
        except KeyError:
            description = None

        try:
            id = job['id']
        except KeyError:
            id = None

        try:
            createdAt = job['updated_at']
        except KeyError:
            createdAt = None

        try:
            link = job['absolute_url']
        except KeyError:
            link = None

        try:
            team = job['departments'][0]['name']
        except KeyError:
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

    adept_dict = support_functions.create_dict('adept', jobs)
    return adept_dict

if __name__ == "__main__":
    main()



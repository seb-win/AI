import requests
import json
from datetime import date
from bs4 import BeautifulSoup
import support_functions

def main():
    headers = {
        'authority': 'inflection.ai',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://inflection.ai/careers',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    header_single = {
        'authority': 'boards.greenhouse.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
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

    params = {
        'maxVacanciesDisplayed': 'null',
    }

    response = requests.get('https://inflection.ai/api/currentVacancies', params=params, headers=headers)
    json_obj = json.loads(response.text)

    jobs =[]
    for job in json_obj:
        try:
            jobTitle = job['title']
        except:
            jobTitle = None

        try:
            loc = job['location'].split(",")
            city = loc[0].strip()
            country = loc[-1].strip()
        except:
            city = None
            country = None

        try:
            link = job['url']
        except:
            link = None

        try:
            response = requests.get('https://boards.greenhouse.io/inflectionai/jobs/4230943006', headers=header_single)
            content_html = BeautifulSoup(response.text, 'html.parser').find('div', {'id': 'content'})
            description = content_html.get_text()
        except:
            description = None
        job_details = {'jobTitle': jobTitle,
                        'country': country, 
                        'location': city, 
                        'commitment': None, 
                        'workplaceType': None, 
                        'description': support_functions.remove(description), 
                        'id': None,
                        'createdAt': date.today(),
                        'team': None,
                        'link': link}
        jobs.append(job_details)

    inflection_dict = support_functions.create_dict('inflection', jobs)

    return inflection_dict

if __name__ == "__main__":
    main()
 
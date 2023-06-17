import requests
import json
from bs4 import BeautifulSoup
import support_functions

def main():
    headers = {
        'authority': 'boards-api.greenhouse.io',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.glean.com',
        'referer': 'https://www.glean.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/gleanwork/departments/', headers=headers)

    json_obj = json.loads(response.text)

    all_jobs = []
    jobCount = 0

    for dep in json_obj['departments']:
        category = {'name': dep['name'],
                    'jobs': None}
        jobs = []
        if len(dep['jobs']) == 0:
            category['jobs'] = dep['jobs']
        else:
            for job in dep['jobs']:

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
                    job_desc = requests.get(link).text
                    content = BeautifulSoup(job_desc, 'html.parser').find('div', {'id': 'content'})
                    description = support_functions.remove(content.get_text())
                except:
                    description = None

                try:
                    createdAt = job['updated_at']
                except:
                    createdAt = None

                try:
                    team = dep['name']
                except:
                    team = None

                job_details = {'jobTitle': jobTitle,
                            'country': None, 
                            'location': location, 
                            'commitment': None, 
                            'workplaceType': None, 
                            'description': description, 
                            'id': id,
                            'createdAt': createdAt,
                            'team': team,
                            'link': link}
                jobs.append(job_details)
            category['jobs'] = jobs
            jobCount += len(jobs)
        all_jobs.append(category)
    
    glean_dict = {'company': 'glean',
                    'jobCount': jobCount,
                    'jobs': all_jobs}
    return glean_dict

if __name__ == "__main__":
    print(main())



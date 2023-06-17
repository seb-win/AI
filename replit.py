import requests
import json
from datetime import date
import support_functions

def main():
    headers = {
        'authority': 'api.ashbyhq.com',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://replit.com',
        'referer': 'https://replit.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get('https://api.ashbyhq.com/posting-api/job-board/replit', headers=headers)

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
            location = job['location']
        except:
            location = None

        try:
            commitment = job['employmentType']
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
            description = support_functions.remove(job['descriptionPlain'])
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            link = job['jobUrl']
        except:
            link = None

        try:
            team = job['department']
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

    replit_dict = support_functions.create_dict('replit', jobs)

    return replit_dict

if __name__ == "__main__":
    main()





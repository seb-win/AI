import requests
import json
import traceback

def main():
    url = "https://api.lever.co/v0/postings/Anthropic"

    querystring = {"group":"team","mode":"json"}

    payload = ""
    headers = {
        "Accept": "*/*",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.anthropic.com",
        "Referer": "https://www.anthropic.com/careers",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    json_response = json.loads(response.text)

    all_jobs = []

    for obj in json_response:
        job = []
        for item in obj['postings']:
            try:
                jobTitle = item['text']
            except KeyError:
                jobTitle = None

            try:
                country = item['country']
            except KeyError:
                country = None

            try:
                location = item['categories']['location']
            except KeyError:
                location = None

            try:
                commitment = item['categories']['commitment']
            except KeyError:
                commitment = None

            try:
                workplaceType = item['workplaceType']
            except KeyError:
                workplaceType = None

            try:
                description = item['lists']
            except KeyError:
                description = None

            try:
                id = item['id']
            except KeyError:
                id = None

            try:
                createdAt = item['createdAt']
            except KeyError:
                createdAt = None

            try:
                link = item['hostedUrl']
            except KeyError:
                link = None

            try:
                team = item['categories']['team']
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
            job.append(job_details)

        category = {'category': obj['title'],
                    'jobs': job}
        
        all_jobs.append(category)
    
    anthropic_dict = {'company': 'anthropic',
                    'jobCount': len(json_response),
                    'jobs': all_jobs}
    return anthropic_dict

if __name__ == "__main__":
    main()
    

    
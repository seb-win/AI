import requests
import json
import support_functions

def check_remote(data):
    if data == 'true':
        remote = 'remote'
    else:
        remote = 'office'
    return remote

def main():
    headers = {
        'authority': 'apply.workable.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'content-type': 'application/json',
        'origin': 'https://apply.workable.com',
        'referer': 'https://apply.workable.com/huggingface/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }


    json_data = {
        'query': '',
        'location': [],
        'department': [],
        'worktype': [],
        'token': "",
        'remote': [],
    }

    response = requests.post(
        'https://apply.workable.com/api/v3/accounts/huggingface/jobs',
        headers=headers,
        json=json_data,
    )

    json_obj = json.loads(response.text)

    allResults = json_obj['results']

    while 'nextPage' in json_obj:
        token = json_obj['nextPage']
        json_data = {
        'query': '',
        'location': [],
        'department': [],
        'worktype': [],
        'token': token,
        'remote': [],
        }

        response = requests.post(
        'https://apply.workable.com/api/v3/accounts/huggingface/jobs',
        headers=headers,
        json=json_data,
        )

        json_obj = json.loads(response.text)

        allResults += json_obj['results']

    jobs = []
    for job in allResults:
        try:
            jobTitle = job['title']
        except:
            jobTitle = None

        try:
            country = job['location']['country']
        except:
            country = None

        try:
            location = job['location']['city']
        except:
            location = None

        try:
            commitment = None
        except:
            commitment = None

        try:
            workplaceType = check_remote(job['remote'])
        except:
            workplaceType = None

        try:
            id = job['id']
        except:
            id = None

        try:
            response = requests.get(f'https://apply.workable.com/api/v2/accounts/huggingface/jobs/{job["shortcode"]}',headers=headers)
            desc_json = json.loads(response.text)
            description = desc = desc_json['description']
        except:
            description = None

        try:
            createdAt = job['published']
        except:
            createdAt = None

        try:
            link = f'https://apply.workable.com/huggingface/j/{job["shortcode"]}'
        except:
            link = None

        try:
            team = job['department'][0]
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

    huggingface_dict = support_functions.create_dict('huggingface',jobs)

    return huggingface_dict

if __name__ == "__main__":
    main()



    

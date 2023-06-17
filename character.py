import requests
import json
from datetime import date
from bs4 import BeautifulSoup

def main():
    headers = {
        'authority': 'jobs.ashbyhq.com',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'apollographql-client-name': 'frontend_non_user',
        'apollographql-client-version': '0.1.0',
        'content-type': 'application/json',
        'origin': 'https://jobs.ashbyhq.com',
        'referer': 'https://jobs.ashbyhq.com/character',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-datadog-origin': 'rum',
        'x-datadog-parent-id': '5373970366697007937',
        'x-datadog-sampling-priority': '1',
        'x-datadog-trace-id': '7885814523826259968',
    }

    params = {
        'op': 'ApiJobBoardWithTeams',
    }

    json_data = {
        'operationName': 'ApiJobBoardWithTeams',
        'variables': {
            'organizationHostedJobsPageName': 'character',
        },
        'query': 'query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }\n    jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\n  locationId\n  locationName\n  __typename\n}',
    }

    def get_json_data(id):
        json_data = {
            'operationName': 'ApiJobPosting',
            'variables': {
                'organizationHostedJobsPageName': 'character',
                'jobPostingId': str(id),
            },
            'query': 'query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {\n  jobPosting(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n    jobPostingId: $jobPostingId\n  ) {\n    id\n    title\n    departmentName\n    locationName\n    employmentType\n    descriptionHtml\n    isListed\n    isConfidential\n    teamNames\n    applicationForm {\n      ...FormRenderParts\n      __typename\n    }\n    surveyForms {\n      ...FormRenderParts\n      __typename\n    }\n    secondaryLocationNames\n    compensationTierSummary\n    compensationTiers {\n      id\n      title\n      tierSummary\n      __typename\n    }\n    compensationTierGuideUrl\n    scrapeableCompensationSalarySummary\n    compensationPhilosophyHtml\n    applicationLimitCalloutHtml\n    __typename\n  }\n}\n\nfragment JSONBoxParts on JSONBox {\n  value\n  __typename\n}\n\nfragment FileParts on File {\n  id\n  filename\n  __typename\n}\n\nfragment FormFieldEntryParts on FormFieldEntry {\n  id\n  field\n  fieldValue {\n    ... on JSONBox {\n      ...JSONBoxParts\n      __typename\n    }\n    ... on File {\n      ...FileParts\n      __typename\n    }\n    ... on FileList {\n      files {\n        ...FileParts\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  isRequired\n  descriptionHtml\n  __typename\n}\n\nfragment FormRenderParts on FormRender {\n  id\n  formControls {\n    identifier\n    title\n    __typename\n  }\n  errorMessages\n  sections {\n    title\n    descriptionHtml\n    fieldEntries {\n      ...FormFieldEntryParts\n      __typename\n    }\n    __typename\n  }\n  sourceFormDefinitionId\n  __typename\n}',
        }
        return json_data

    response = requests.post(
        'https://jobs.ashbyhq.com/api/non-user-graphql',
        params=params,
        headers=headers,
        json=json_data,
    )

    json_obj =json.loads(response.text)

    categories = []
    for obj in json_obj['data']['jobBoard']['teams']:
        category = {'name': obj['name'],
                    'id': obj['id'],
                    'jobs': None}

    all_jobs = []

    jobs = []
    for item in json_obj['data']['jobBoard']['jobPostings']:

        try:
            jobTitle = item['title']
        except:
            jobTitle = None

        try:
            country = None
        except:
            country = None

        try:
            location = item['locationName']
        except:
            location = None

        try:
            commitment = item['employmentType']
        except:
            commitment = None

        try:
            workplaceType = None
        except:
            workplaceType = None

        try:
            id = item['id']
        except:
            id = None

        try:
            json_data = get_json_data(id)
            response = requests.post('https://jobs.ashbyhq.com/api/non-user-graphql',json=json_data)
            desc_json = json.loads(response.text)
            descriptionHtml = desc_json['data']['jobPosting']['descriptionHtml']
            description = BeautifulSoup(descriptionHtml, 'html.parser').get_text() 
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            link = f"https://jobs.ashbyhq.com/character/{item['id']}"
        except:
            link = None

        try:
            team = item['teamId']
        except:
            team = None


        job_details = {'jobTitle': jobTitle,
                        'country': None, 
                        'location': location, 
                        'commitment': commitment, 
                        'workplaceType': None, 
                        'description': description, 
                        'id': id,
                        'createdAt': date.today(),
                        'team': team,
                        'link': link}
        jobs.append(job_details)

    for obj in json_obj['data']['jobBoard']['teams']:
        categoryId = obj['id']
        catJobs = []
        for job in jobs:
            if job['team'] == categoryId:
                catJobs.append(job)

        category = {'name': obj['name'],
                    'id': obj['id'],
                    'jobs': catJobs}
        all_jobs.append(category)

    characterai_dict = {'company': 'charakterai',
                    'jobCount': len(jobs),
                    'jobs': all_jobs}
    return characterai_dict

if __name__ == "__main__":
    main()






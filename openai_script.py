from bs4 import BeautifulSoup
import json
import requests
import support_functions
from datetime import date

def main():
    html_file = requests.get('https://openai.com/careers/search')

    soup = BeautifulSoup(html_file.text, 'html.parser')

    all = soup.find("section", {"id": "jobResultsSection0"})
    li_elements = all.find_all("li")


    jobs = []
    for li in li_elements:
        try:
            jobTitle = li.find("h3").text
        except:
            jobTitle = None
        
        try:   
            link = f"https://openai.com{li.find('a').get('href')}"
        except:
            link = None
        
        try:
            res = li.find("span").text.replace("â", ",").replace("\x80\x94", "")
            result_list = res.split(",")
            location = result_list[0].strip()
            country = result_list[2].strip()
            team = result_list[3].strip()
        except:
            location = None
            country = None
            team = None

        try:
            job_desc = requests.get(link).text
            content = BeautifulSoup(job_desc, 'html.parser').find('div', class_='ui-description ui-richtext')
            description = support_functions.remove(content.get_text())
        except:
            description = None

        job_details = {'jobTitle': jobTitle,
                        'country': country, 
                        'location': location, 
                        'commitment': None, 
                        'workplaceType': None, 
                        'description': description, 
                        'id': link,
                        'createdAt': date.today(),
                        'team': team,
                        'link': link}
        jobs.append(job_details)
        

    openai_dict = support_functions.create_dict('openai', jobs)

    return openai_dict

if __name__ == "__main__":
    main()





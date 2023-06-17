from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import support_functions


def main():
    options = Options()
    options.add_argument("--headless=new")  # Run in headless mode without opening a browser window

    # Replace 'path/to/chromedriver' with t‚he actual path to the ChromeDriver executable
    service = Service('/Users/sebastianwinkler/Documents/chromedriver_mac_arm64/chromedriver')
    driver = webdriver.Chrome(options=options)

    driver.get('https://careers.lightricks.com/careers?query=&office=all&department=all')  # Replace with the actual URL containing the HTML
    time.sleep(10)
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.job_collection_item')

    jobs = []
    for element in elements:
        title = element.find_element(By.CSS_SELECTOR, 'h2.list_js_title').text
        parent_dep = element.find_element(By.CSS_SELECTOR, 'div.list_js_parent_department').text
        child_dep = element.find_element(By.CSS_SELECTOR, 'div.list_js_child_department').text
        location = element.find_element(By.CSS_SELECTOR, 'div.list_js_office').text
        link = element.find_element(By.CSS_SELECTOR, 'a.job_collection_link_block').get_attribute('href')

        try:
            jobTitle = element.find_element(By.CSS_SELECTOR, 'h2.list_js_title').text
        except:
            jobTitle = None

        try:
            country = None
        except:
            country = None

        try:
            location = element.find_element(By.CSS_SELECTOR, 'div.list_js_office').text
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
            id = None
        except:
            id = None

        try:
            description = None
        except:
            description = None

        try:
            createdAt = date.today()
        except:
            createdAt = None

        try:
            link = element.find_element(By.CSS_SELECTOR, 'a.job_collection_link_block').get_attribute('href')

        except:
            link = None

        try:
            team = element.find_element(By.CSS_SELECTOR, 'div.list_js_parent_department').text
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

    for job in jobs:
        driver.get(link)
        time.sleep(5)
        description = driver.find_element(By.CSS_SELECTOR, 'div.data-element')
        job['description'] = description.text

    driver.quit()

    lightricks_dict = support_functions.create_dict('lightricks', jobs)

    return lightricks_dict

if __name__ == "__main__":
    main()
import re

def remove(text):
    pattern = r"\n\s*\n"  # Regex pattern to match empty lines
    text_without_empty_lines = re.sub(pattern, "\n", text)
    lines = text_without_empty_lines.split("\n")
    lines_without_spaces = [re.sub(r"^\s+", "", line) for line in lines]
    return "\n".join(lines_without_spaces)

def create_dict(comp_name, jobs):
    all_jobs = []
    categories = []
    for job in jobs:
        categories.append(job['team'])

    categories = list(set(categories))

    for cat in categories:
        catJobs = []
        for job in jobs:
            if job['team'] == cat:
                catJobs.append(job)
        
        category = {'name': cat,
                    'jobs': catJobs}
        
        all_jobs.append(category)

    company_dict = {'company': comp_name,
                    'jobCount': len(jobs),
                    'jobs': all_jobs}
    return company_dict
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the B Corporation directory
url = 'https://www.bcorporation.net/en-us/find-a-b-corp/'

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store the company data
companies = []

# Extracting company data
for company in soup.find_all('div', class_='p-4'):
    name_span = company.find('span', {'data-testid': 'company-name-desktop'})
    description_p = company.find('p', class_='mt-4 line-clamp-3')

    if name_span and description_p:
        name = name_span.text.strip()
        description = description_p.text.strip()
        companies.append({'Name': name, 'Description': description})

# Convert the list to a DataFrame
df = pd.DataFrame(companies)

# Save the DataFrame to a CSV file
df.to_csv('b_corp_companies.csv', index=False)

print("List of companies has been saved to b_corp_companies.csv")

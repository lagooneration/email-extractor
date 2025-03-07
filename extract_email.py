import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_email(text):
    """Extracts the first valid email from text using regex"""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def get_email_from_website(url):
    """Fetches and scrapes email from the given website"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None  # Skip if the page is not reachable

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        email = extract_email(text)
        
        if not email:  
            # If no email, try finding a contact page link
            for link in soup.find_all("a", href=True):
                if "contact" in link["href"].lower():
                    contact_url = link["href"]
                    if not contact_url.startswith("http"):
                        contact_url = url + "/" + contact_url.strip("/")
                    return get_email_from_website(contact_url)
        
        return email
    except Exception as e:
        return None

# Read Excel file containing college websites
df = pd.read_excel("colleges.xlsx")

# Ensure the column name is correct
colleges = df["Website"].tolist()  

emails = []
for college in colleges:
    email = get_email_from_website(college)
    emails.append(email)
    print(f"Extracted: {email} from {college}")

# Save results to Excel
df["Email"] = emails
df.to_excel("emails.xlsx", index=False)

print("Scraping completed! Results saved in emails.xlsx")

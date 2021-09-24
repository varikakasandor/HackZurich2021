import requests
from bs4 import BeautifulSoup

base_url="https://contracts.onecle.com"
url = f"{base_url}/type/2.shtml"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

new_urls=[f"{base_url}{a}" for a in list(soup.find_all('a', href=True))[18:-45]]
    

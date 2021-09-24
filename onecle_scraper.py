import requests
from bs4 import BeautifulSoup
import multiprocess as mp
import html2text



def get_all_text(contract_url):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    page = requests.get(contract_url)
    all_text=converter.handle(page.text)
    return all_text


if __name__=="__main__":

    base_url="https://contracts.onecle.com"
    url = f"{base_url}/type/2.shtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_urls=[f"{base_url}{a['href']}" for a in list(soup.find_all('a', href=True))[18:-45]][:mp.cpu_count()]
    with mp.Pool(mp.cpu_count()) as pool:
        texts=pool.map(get_all_text, new_urls)
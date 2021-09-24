import requests
from bs4 import BeautifulSoup
import multiprocess as mp
import html2text
import re

from keywords import *

base_url="https://contracts.onecle.com"

def get_all_text(contract_url):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    page = requests.get(contract_url)
    all_text_from_page=converter.handle(page.text)
    sentences=re.split('.', all_text_from_page)
    return sentences


if __name__=="__main__":
    url = f"{base_url}/type/2.shtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_urls=[f"{base_url}{a['href']}" for a in list(soup.find_all('a', href=True))[18:-45]]
    with mp.Pool(mp.cpu_count()) as pool:
        sentences_per_contract=pool.map(get_all_text, new_urls)

    sentences=flat_list = [item for sublist in sentences_per_contract for item in sublist]
    with open("a_file.txt", "w") as output_file:
        for sentence in sentences:
            output_file.write(sentence + "\n")

import requests
from bs4 import BeautifulSoup
import multiprocess as mp
import html2text
import re
import pandas as pd

from keywords import *

base_url="https://contracts.onecle.com"

def is_right(sentence):
    if ('may' in sentence) and ('may not' not in sentence):
        return True
    if any(right in sentence for right in primary_rights):
        return True
    if any(right in sentence for right in secondary_rights) and any(helper in sentence for helper in right_helpers):
        return True
    return False

def is_duty(sentence):
    if any(duty in sentence for duty in primary_duties):
        return True
    if any(duty in sentence for duty in secondary_duties) and any(helper in sentence for helper in duty_helpers):
        return True
    return False

def clean_sentence(sentence):
    sentence=sentence.strip()
    sentence=sentence.replace("\n", " ")
    sentence=re.sub(' +', ' ', sentence)
    return f"{sentence}."

def get_all_text(contract_url, idx):
    try:
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        page = requests.get(contract_url)
        all_text_from_page=converter.handle(page.text)
        sentences=re.split('\.', all_text_from_page)
        kept_sentences=[]
        for sentence in sentences:
            sentence=clean_sentence(sentence)
            if is_right(sentence):
                kept_sentences.append((sentence,'Right'))
            elif is_duty(sentence):
                kept_sentences.append((sentence,'Duty'))
        print(f"{idx} is done.")
        return kept_sentences
    except Exception as e: #Maybe it does not accept more connections
        print(e)
        return []


if __name__=="__main__":
    url = f"{base_url}/type/2.shtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_urls=[f"{base_url}{a['href']}" for a in list(soup.find_all('a', href=True))[18:-45]]
    with mp.Pool(mp.cpu_count()) as pool:
        sentences_per_contract=pool.starmap(get_all_text, zip(new_urls,range(len(new_urls))))

    sentences = [item for sublist in sentences_per_contract for item in sublist]
    df=pd.DataFrame(sentences,columns=['Sentence','PredictedType'])
    df.to_csv('Sentences_to_annotate.csv', index=False)

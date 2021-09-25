import requests
from bs4 import BeautifulSoup
import multiprocess as mp
import html2text
import re
import pandas as pd
import random
    


from keywords import *

base_url="https://contracts.onecle.com"

def exactly_in(sentence, word):
    return (f"{word} " in sentence) or (f"{word}." in sentence)

def is_right(sentence):
    if exactly_in(sentence,'may') and exactly_in(sentence,'may not'):
        return True
    if any(exactly_in(sentence,right) for right in primary_rights):
        return True
    if any(exactly_in(sentence,right) for right in secondary_rights) and any(exactly_in(sentence,helper) for helper in right_helpers):
        return True
    return False

def is_duty(sentence):
    if any(exactly_in(sentence,duty) for duty in primary_duties):
        return True
    if any(exactly_in(sentence,duty) for duty in secondary_duties) and any(exactly_in(sentence,helper) for helper in duty_helpers):
        return True
    return False

def clean_sentence(sentence):
    sentence=sentence.strip()
    sentence=sentence.replace("\n", " ")
    sentence=re.sub(' +', ' ', sentence)
    return f"{sentence}."

def get_main_part_of_sentence(sentence):
    return sentence
    #TODO

def get_all_text(contract_url, idx):
    try:
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        page = requests.get(contract_url)
        all_text_from_page=converter.handle(page.text)
        sentences=re.split('\.|\*|\||:', all_text_from_page)
        kept_sentences=[]
        for original_sentence in sentences:
            full_sentence=clean_sentence(original_sentence)
            main_part_of_sentence=get_main_part_of_sentence(full_sentence)
            if is_right(main_part_of_sentence):
                kept_sentences.append((main_part_of_sentence, full_sentence, contract_url, 'Right'))
            elif is_duty(main_part_of_sentence):
                kept_sentences.append((main_part_of_sentence, full_sentence, contract_url, 'Duty'))

        print(f"{idx} is done.")
        return kept_sentences,(contract_url,all_text_from_page)
    except Exception as e: #Maybe it does not accept more connections
        print(f"{idx} has thrown {e}")
        return [], None


if __name__=="__main__":
    url = f"{base_url}/type/2.shtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    new_urls=[f"{base_url}{a['href']}" for a in list(soup.find_all('a', href=True))[18:-45]]
    with mp.Pool(mp.cpu_count()) as pool:
        sentences_per_contract=pool.starmap(get_all_text, zip(new_urls,range(len(new_urls))))

    sentences = [item for l,_ in sentences_per_contract for item in l]
    sentences_df=pd.DataFrame(sentences,columns=['SentenceMain','SentenceFull','ID','PredictedType'])
    sentences_df.to_csv('Sentences_to_annotate.csv', index=False)

    full_texts = [item for _,item in sentences_per_contract if item is not None]
    full_texts_df=pd.DataFrame(full_texts,columns=['ID','FullText'])
    full_texts_df.to_csv('Full_texts.csv', index=False)

"""Ryan Cox     ID#31953949"""
"""Arya Kashani ID#10847777"""
import re
import atexit
import logging
import json
import urllib.request
import math
import operator

from pip._vendor import requests
from pip._vendor.requests.packages.urllib3.util import url

from bs4 import BeautifulSoup

def tokenize(search):
    words = search.split()
    tokens = {}
    for each in words:
        new_word = ""
        for letter in each:
            if re.match("[A-Za-z0-9]$", letter):
                new_word += letter
            else:
                new_word = new_word.lower()
                if len(new_word) >= 1:
                    if new_word in tokens:
                        tokens[new_word][0] = tokens[new_word][0] + 1
                    else:
                        tokens[new_word] = [1]
                new_word = ""
        new_word = new_word.lower()
        if len(new_word) >= 1:
            if new_word in tokens:
                tokens[new_word][0] = tokens[new_word][0] + 1
            else:
                tokens[new_word] = [1]
    return tokens, len(words)


def create(json_text):
    inverted_index = {}
    for key,url in json_text.items():
        key_split = key.split('/')
        html = open("WEBPAGES_RAW/"+key_split[0]+"/"+key_split[1], 'r', encoding = "utf-8")
        
        soup = BeautifulSoup(html, features="lxml") #https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python/3987802
        for script in soup(["script", "style"]): #whole process of retrieving the text was taken from this link
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        tokens, len_txt = tokenize(text)
        
        for tok, tf in tokens.items():
            if tok not in inverted_index:
                inverted_index[tok] = []
                inverted_index[tok].append([key, tf[0] / len_txt])
            else:
                inverted_index[tok].append([key, tf[0] / len_txt])
                
    total_docs = len(json_text.items())
    for i in inverted_index:
        for j in inverted_index[i]:
            idf = math.log10(total_docs / len(inverted_index[i]))
            j[1] = j[1] * idf
                             
    return inverted_index


if __name__ == "__main__":
    json_text = json.load(open("WEBPAGES_RAW/bookkeeping.json", 'r')) #https://linuxconfig.org/how-to-parse-data-from-json-into-python
    inverted_index = create(json_text)
    with open('inverted_index.json', 'w') as index_file: #https://stackoverflow.com/questions/17043860/python-dump-dict-to-json-file
        json.dump(inverted_index, index_file)
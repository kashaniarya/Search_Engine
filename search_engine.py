"""Ryan Cox     ID#31953949"""
"""Arya Kashani ID#10847777"""
import re
import atexit
import logging
import json
import urllib.request
import math
import operator
from bs4 import BeautifulSoup

from pip._vendor import requests
from pip._vendor.requests.packages.urllib3.util import url

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
                    tokens[new_word] = []
                new_word = ""
        new_word = new_word.lower()
        if len(new_word) >= 1:
            tokens[new_word] = []
    return tokens

def _top_20(mergedIndex):
    json_text = json.load(open("WEBPAGES_RAW/bookkeeping.json", 'r'))
    top20Index = []
    for each in {k: v for k, v in sorted(mergedIndex.items(), key=lambda x: x[1])}:
        if len(top20Index) < 20:
            actual_url = json_text[each]
            top20Index.append(actual_url)
    
    return top20Index

if __name__ == "__main__":    
    search = ""
    inverted_index = json.load(open("inverted_index.json", 'r')) #https://linuxconfig.org/how-to-parse-data-from-json-into-python
    search = input("Search, enter -1 to quit: ")
    
    while search != "-1":
        tokens = tokenize(search)
        
        docs = {}
        for tok in tokens:
            temp_values = inverted_index[tok]
            for each_ref in temp_values:
                if each_ref[0] in docs.keys():
                    docs[each_ref[0]] += each_ref[1]
                else:
                    docs[each_ref[0]] = each_ref[1]
        top_20_index = _top_20(docs)
        
        count = 0
        for each in reversed(top_20_index):
            count += 1
            print("{} - {}".format(count, each))
        

        search = input("Search, enter -1 to quit: ")
    print("Exited search engine")
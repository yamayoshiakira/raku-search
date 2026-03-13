# application/tools/mecab.py

import requests
import urllib

MECAB_URI = "http://140.227.225.166/mecab"  #WebARENA

def get(sentence):

    keywords = []

    url = MECAB_URI + "?q=" + urllib.parse.quote(sentence)
    try:
        response = requests.get(url, timeout=3)

        if response.status_code == 200:
            res = response.json()
    
            words = []
            for part in res['parts']:
                word, vals = part.popitem()
                if (len(word) > 1
                        and vals[0] == u"名詞"
                        and vals[1] != u"サ変接続"):
                    words.append(word)
            
            if len(words) > 1:
                pre_word = words.pop(0)
                for word in words:
                    key_word = pre_word + " " + word
                    pre_word = word
        
                    if key_word not in keywords:
                        keywords.append(key_word)
    except:
        pass

    return keywords

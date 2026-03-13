 # raku-tabi application/views.py

import json
import time
import urllib

#from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, redirect, render_template, abort

from application import app

from models import Keyword3 as Keyword
from tools import rakuapi, mecab


LIMIT = 50


@app.route('/test')
def test():

    RakuAppId = "0f53734a-e88d-427a-a59c-d8a6ad0e3954"
    RakuSAK = "pk_w7zMTbmJexNTp2NN0MKhuWSehuM8j2ClhcMz73eDR7t"
    RakuAffId = ""
    AppURL = "https://raku-search.appspot.com/" 

    import requests


    try:
        base_url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"
        params = {
            "applicationId": RakuAppId,
            "accessKey": RakuSAK,    
            "format": "json",
            "genreId": "555086",        
            "keyword": "猫",
        }
        headers = {
            "Referer": AppURL,
            "Origin": AppURL
        }
        response = requests.get(base_url, params=params, headers=headers)
        #response = requests.get(url, headers=headers)
        # デバッグ用にステータスコードも出すにゃ
        print(f"Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"エラーだにゃ: {e}")

    from google.cloud import secretmanager
    sm_client = secretmanager.SecretManagerServiceClient()
    
    def get_secret(secret_id):
        name = f"projects/242870823131/secrets/{secret_id}/versions/latest"
        response = sm_client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    RakuAppId = get_secret("RakuAppId")
    RakuSAK = get_secret("RakuSAK")
    RakuAffId = get_secret("RakuAffId")
    print("a>>", RakuAppId)
    print(RakuSAK)
    print(RakuAffId)

    import os
    #PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "242870823131")
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    print(PROJECT_ID)

    def get_secret2(secret_id):
        name = sm_client.secret_version_path(PROJECT_ID, secret_id, "latest")
        return sm_client.access_secret_version(request={"name": name}).payload.data.decode("UTF-8")

    RakuAppId2 = get_secret("RakuAppId")
    print("b>>", RakuAppId2)

    return "ok22"


@app.route('/')
def home_page():

    q_options = {
        'order': "-created",
        'limit': LIMIT,
    }
    keywords, q_options = Keyword.fetch(keys_only=True, **q_options)
    url_query = "?" + urllib.parse.urlencode(q_options, doseq=True)

    content = {
        'keywords': keywords,
        'url_query': url_query,
    }

    return render_template('home.html', **content)


@app.route('/list')
def list_page():

    q_options = request.args.to_dict()
    keywords, q_options = Keyword.fetch(keys_only=True, **q_options)
    url_query = "?" + urllib.parse.urlencode(q_options, doseq=True)

    content = {
        'keywords': keywords,
        'url_query': url_query,
    }
    return render_template('list.html', **content)


@app.route('/search')
def search():
    """ /search?q=<keyword> """
    q = request.args.get('q')
    url = "/word/" + "/".join(q.split()) + "/"
    return redirect(url)


@app.route('/word/<path:path>/')
def word_page(path):
    """ /word/<keyword>/ """

    word = " ".join(path.split("/"))
    hits, products, _ = rakuapi.item_search(word)

    if request.referrer:
        keyword = Keyword.get(word)
        if keyword:
            keyword.created = int(time.time())  # update utc_now
        else:
            keyword = Keyword(word)
        keyword.put()

    content = {
        'word': word,
        'hits': hits,
        'products': products,
    }
    return render_template('word.html', **content)

@app.route('/w/<path:path>/')
def w_page(path):
    url = "/word/" + path + "/"
    return redirect(url)


@app.route('/item/<path:path>/')
def item_page(path):
    """ /item/<scode>/<item_name>/?key=val """

    try:
        path = path.split("/")
        code = path[0]
        name = path[1] if path[1:] else ""
    
        product = rakuapi.item_lookup(code)
    
        keywords = [Keyword(word) for word in mecab.get(product['name'])]
        product['keywords'] = keywords
    
        content = {
            'product': product,
        }
        return render_template('item.html', **content)

    except:
        abort(404)

@app.route('/i/<path:path>/')
def i_page(path):
    url = "/item/" + path + "/"
    return redirect(url)


    '''
    executor = ThreadPoolExecutor()
    future1 = executor.submit(webapi.lookup, scode)
    #future2 = executor.submit(janome.get, item_name)
    future2 = executor.submit(mecab.get, item_name)
    #future2 = executor.submit(kwpick.get, item_name)
    executor.shutdown()

    if future1.result():
        item = Item(scode)
        if request.referrer:
            item.put()
        item.add(future1.result())
        item.keywords = future2.result()
        content = {
            'item': item,
        }
        return render_template('item.html', **content)

    else:
        abort(404)
    '''


@app.route('/sitemap.xml')
def sitemap():
    q_options = {
        'order': "-created",
        'limit': 1000,
    }
    keywords, _ = Keyword.fetch(keys_only=True, **q_options)
    content = {
        'keywords': keywords,
    }
    return render_template('sitemap.xml', **content)



@app.route('/cron_day')
def cron_day():
    """ Get kakaku.com keyword and Put datastore"""
    '''
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    def dsput(word):
        keyword = Keyword.get(word)
        if not keyword:
            keyword = Keyword(word)
            keyword.put()
            #print(a_text, keyword.key)
    
    now = datetime.today()
    i = now.weekday() + 1

    url = "https://kakaku.com/keyword/page={0}/".format(i)
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for a in soup.select('a[href^="/search_results/"]'):
            executor.submit(dsput, a.text)
    '''
    return "ok"


@app.route('/cron_hour')
def cron_hour():
    """ delete old data """

    from google.cloud import datastore
    client = datastore.Client()

    query = client.query()
    query.keys_only()
    query.kind = 'Word'

    q_options = dict(limit=500)
    query_iter = query.fetch(**q_options)

    keys = [entity.key for entity in query_iter]
    client.delete_multi(keys)
    
    return "delete ok"


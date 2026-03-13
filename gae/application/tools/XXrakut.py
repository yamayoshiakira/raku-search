# raku-tabi application/tools/rakut.py

import json
import urllib
import requests


RakuDevId = "1032233083022704410"
RakuSAK   = "898d46c5ff1d35230d878b5c9bba33830f6289f9"
RakuAffId = "0fd71c63.dc6e657e.0fd71c64.eff2b6f0"


def item_shaping(item):

    name = item['name'].replace("　", " ")
    item['short_name'] = name if len(name) < 20 else name[:20] + "..."

    capt = item['caption'].replace("　", " ")
    item['description'] = capt if len(capt) < 100 else capt[:100] + "..."
    
    return item


def item_search(word, **kwargs):

    hits = 0
    items = []

    try:
        base_url = "https://app.rakuten.co.jp/services/api/Travel/KeywordHotelSearch/20170426?"
        req = {
            'applicationId': RakuDevId,
            'affiliateId': RakuAffId,
            'formatVersion': 2,
            'keyword': word,
        }
        req.update(kwargs)
        url = base_url + urllib.parse.urlencode(req)
        resp = requests.get(url)
        data = resp.json()
    
        hits = data['pagingInfo']['recordCount']
        if hits > 0:
            for value in data['hotels']:
                info = value[0]['hotelBasicInfo']
                if info['hotelMinCharge'] is not None:
                    item = {
                        'code': info['hotelNo'],
                        'name': info['hotelName'],
                        'caption': info['hotelSpecial'] + "【アクセス】" +info['access'],
                        'img': info['hotelThumbnailUrl'],
                        'url': info['hotelInformationUrl'],
                        'price': info['hotelMinCharge'],
                        'review': info['reviewCount'] if info['reviewCount'] else 0,
                        'rating': float(info['reviewAverage']) if info['reviewAverage'] else 0.0,
                        'source': info['address1'],
                        'supply': info['address2'],
                    }
                    item = item_shaping(item)
                    items.append(item)
            items = sorted(items, key=lambda item: item['price'])

    except:
        pass
 
    return (hits, items)


def item_lookup(code):

    item = {}

    try:
        base_url = "https://app.rakuten.co.jp/services/api/Travel/HotelDetailSearch/20170426?"
        req = {
        	'applicationId' : RakuDevId,
        	'affiliateId'   : RakuAffId,
        	'formatVersion' : 2,
        	'hotelNo'       : code,
        }
        url = base_url + urllib.parse.urlencode(req)
        resp = requests.get(url)
        data = resp.json()
    
        info = data['hotels'][0][0]['hotelBasicInfo']
        item = {
            'code': info['hotelNo'],
            'name': info['hotelName'],
            'caption': info['hotelSpecial'] + "【アクセス】" +info['access'],
            'img': info['hotelImageUrl'],
            'url': info['hotelInformationUrl'],
            'price': info['hotelMinCharge'],
            'review': info['reviewCount'] if info['reviewCount'] else 0,
            'rating': float(info['reviewAverage']) if info['reviewAverage'] else 0.0,
            'source': info['address1'],
            'supply': info['address2'],
        }
        item = item_shaping(item)

    except:
        pass
    
    return item


# ---------------------------------------------------
#print(json.dumps(res, indent=4, ensure_ascii=False))
#with open('res_search.txt', 'w') as file:
#    json.dump(res, file, indent=4, ensure_ascii=False)

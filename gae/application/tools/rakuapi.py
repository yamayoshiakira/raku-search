# raku-search application/tools/rakuapi.py
# https://webservice.rakuten.co.jp/document/

import json
import urllib
import requests

RakuDevId = "1038069247488126127"
RakuSAK = "aabbf76fc16da4624aab975c16a387c01deaf241"
RakuAffId = "0fd71c63.dc6e657e.0fd71c64.eff2b6f0"


def product_shaping(product):

    name = product['name'].replace("　", " ")
    product['short_name'] = name if len(name) < 20 else name[:20] + "..."

    capt = product['caption'].replace("　", " ")
    product['description'] = capt if len(capt) < 100 else capt[:100] + "..."
    
    return product


def item_search(word, **kwargs):

    ''' hits, products, genreId = rakuapi.item_search(word, genreId="100371") '''

    hits = 0
    products = []
    genreId = "0"

    try:
        base_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
        req = {
            'applicationId': RakuDevId,
            'affiliateId': RakuAffId,
            'formatVersion': 2,
            'genreInformationFlag': 1,
            'availability': 1,
            'imageFlag': 1,
            'minPrice': "100",
            'sort': "-reviewCount",
            'keyword': word,
        }
        req.update(kwargs)
        url = base_url + urllib.parse.urlencode(req)
        res = requests.get(url).json()

        hits = res['count']
        if hits > 0:
            for res_item in res['Items']:
    
                img = res_item['smallImageUrls'][0]
                img = img.replace("thumbnail.image.rakuten.co.jp/@0_mall/","image.rakuten.co.jp/")
                img = img.replace("_ex=64x64", "_ex=80x80")
    
                product = {
                    'code': res_item['itemCode'],
                    'name': res_item['itemName'],
                    'caption': res_item['itemCaption'],
                    'img': img,
                    'url': res_item['affiliateUrl'],
                    'price': res_item['itemPrice'],
                    'review': res_item['reviewCount'],
                    'rating': float(res_item['reviewAverage']),
                    'shopcode': res_item['shopCode'],
                    'shopname': res_item['shopName'],
                }
                product = product_shaping(product)
                products.append(product)

            products = sorted(products, key=lambda product: product['price'])
    
            genres = []
            for child in res['GenreInformation'][0]['children']:
                genre = (int(child['itemCount']), child['genreId'])
                genres.append(genre)
            print(genres, max(genres), max(genres)[1])
            genreId = max(genres)[1] if genres else res['GenreInformation'][0]['current'][0]['genreId']

    except:
        pass

    return (hits, products, genreId)


def item_lookup(code, **kwargs):

    ''' product = rakuapi.item_lookup(code) '''

    product = None

    try:
        base_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
        req = {
            'applicationId': RakuDevId,
            'affiliateId': RakuAffId,
            'formatVersion': 2,
            'itemCode': code,
        }
        req.update(kwargs)
        url = base_url + urllib.parse.urlencode(req)
        res = requests.get(url).json()
    
        if res['count'] == 1:
            res_item = res['Items'][0]
    
            img = res_item['smallImageUrls'][0]
            img = img.replace("thumbnail.image.rakuten.co.jp/@0_mall/","image.rakuten.co.jp/")
            img = img.replace("?_ex=64x64", "")
    
            product = {
                'code': res_item['itemCode'],
                'name': res_item['itemName'],
                'caption': res_item['itemCaption'],
                'img': img,
                'url': res_item['affiliateUrl'],
                'price': res_item['itemPrice'],
                'review': res_item['reviewCount'],
                'rating': float(res_item['reviewAverage']),
                'shopcode': res_item['shopCode'],
                'shopname': res_item['shopName'],
            }
            product = product_shaping(product)

    except:
        pass

    return product


# ---------------------------------------------------
# print(json.dumps(res, indent=4, ensure_ascii=False))
# with open('RES_search.txt', 'w') as file:
#    json.dump(res, file, indent=4, ensure_ascii=False)



    '''
    base_url = "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup?"
    req = {
        'appid': YahooDevId,
        'affiliate_type': "vc",
        'affiliate_id': VcAffId,
        'responsegroup': "large",
        'image_size': "300",
        'itemcode': scode[1:],
    }
    req.update(kwargs)

    url = base_url + urllib.parse.urlencode(req)
    result = requests.get(url)
    res = result.json()
 
    if 'ResultSet' in res:
        if int(res['ResultSet']['totalResultsReturned']) > 0:
            val = res['ResultSet']['0']['Result']['0']
            product = {
                'scode': scode,
                'name': val['Name'],
                'caption': val['Description'],
                'img': val['ExImage']['Url'],
                'url': val['Url'],
                'price': int(val['Price']['_value']),
                'review': int(val['Review']['Count']),
                'rating': float(val['Review']['Rate']),
                'shopcd': val['Store']['Id'],
                'shop': val['Store']['Name'],
                'supplier': "Yahoo!",
            }
            return product

    else:
        return None
    '''




    '''
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
    '''




'''
YahooDevId = "dj00aiZpPWwwU2VhYm5QUlVKcCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjM-"
VcAffId = urllib.parse.quote("http://ck.jp.ap.valuecommerce.com/servlet/referral?sid=3196153&pid=883287436&vc_url=")

SUPPLIER_PREFIX = "Y"
SUPPLIER = "Yahoo!"

GENRE_TOP = 1


def search(word, **kwargs):

    #genre = 1
    #word = "nec"

    genre = kwargs.pop('genre') if 'genre' in kwargs else GENRE_TOP

    base_url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?"
    req = {
        'appid': YahooDevId,
        'affiliate_type': "vc",
        'affiliate_id': VcAffId,
        'genre_category_id': genre,
        'results': 50,
        'sort': "-review_count",
        'price_from': 100,
        'query': word,
    }

    url = base_url + urllib.parse.urlencode(req)
    result = requests.get(url)
    res = result.json()

    hits = 0
    products = []

    if 'hits' in res:
        hits = len(res['hits'])
        if hits > 0:
            genres = [[1],[],[],[],[],[],[],[],[],[]]
            for item in res['hits']:
                product = {
                    'scode': "Y" + item['code'],
                    'name': item['name'],
                    'caption': item['description'],
                    'img': item['image']['small'],
                    'url': item['url'],
                    'price': item['price'],
                    'review': item['review']['count'],
                    'rating': item['review']['rate'],
                    'shopcd': item['seller']['sellerId'],
                    'shop': item['seller']['name'],
                    'supplier': "Yahoo!",
                }
                products.append(product)

                if item['parentGenreCategories']:
                    categories = item['parentGenreCategories']
                    categories.append(item['genreCategory'])
                    for cat in categories:
                        genres[cat['depth']].append(cat['id'])

            for v in reversed(genres):
                if v:
                    counter = Counter(v)
                    genre, cnt = counter.most_common()[0]
                    if float(cnt) / hits >= 0.6:
                        break

        products = sorted(products, key=lambda product: product['price'])


    genre = kwargs.pop('genre') if 'genre' in kwargs else GENRE_TOP

    base_url = "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?"
    req = {
        'appid': YahooDevId,
        'affiliate_type': "vc",
        'affiliate_id': VcAffId,
        'availability': "1",
        'image_size': "80",
        'category_id': "1",
        'hits': "50",
        'sort': "-review_count",
        'price_from': "100",
        'query': word,
    }
    req.update(kwargs)

    url = base_url + urllib.parse.urlencode(req)
    print(url)
    result = requests.get(url)
    res = result.json()

    hits = 0
    products = []

    if 'ResultSet' in res:
        hits = int(res['ResultSet']['totalResultsAvailable'])
        if hits > 0:
            genres = [list() for _ in range(20)]
            for key, val in res['ResultSet']['0']['Result'].items():
                if key.isdigit():
                    product = {
                        'scode': "Y" + val['Code'],
                        'name': val['Name'],
                        'caption': val['Description'],
                        'img': val['Image']['Small'],
                        'url': val['Url'],
                        'price': int(val['Price']['_value']),
                        'review': int(val['Review']['Count']),
                        'rating': float(val['Review']['Rate']),
                        'shopcd': val['Store']['Id'],
                        'shop': val['Store']['Name'],
                        'supplier': "Yahoo!",
                    }
                    products.append(product)

                    for i in range(len(genres)):
                        if str(i) in val['CategoryIdPath']:
                            genres[i].append(
                                val['CategoryIdPath'][str(i)]['Id'])

            for v in reversed(genres):
                if v:
                    counter = Counter(v)
                    genre, cnt = counter.most_common()[0]
                    if float(cnt) / len(products) >= 0.6:
                        break

            products = sorted(products, key=lambda product: product['price'])

    return (genre, hits, products)
'''

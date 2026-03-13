# raku-search application/config.py


class Config(object):

    SECRET_KEY = "7d441f27d431f28567d451d2b5176b"


class Const(object):

    SITE_URL = "raku-search.appspot.com"
    SITE_NAME = "らくサーチ"
    SITE_DESC = "らくサーチへようこそ。食品、家電、ファッション、あなたの欲しいものは何ですか??"

    SITE_AD = {
        'name': "Supported by 楽天ウェブサービス",
        'url': "https://webservice.rakuten.co.jp/",
    }

    GTAG_ID = "UA-353820-xx"
    VERIFICATION = "vfYoSaHGjEiZqU3jLIEyBjYMzraFmy811TLxJRzJ29c"


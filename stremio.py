from flask import Flask, Response, jsonify, url_for, abort
import urllib, re, sys, os, requests, json
from functools import wraps
import urllib.request as urllib2
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import ssl
from lib import embedtamilgun, myfeminist, downscrs

try:
    _create_unverified_https_context = ssl._create_unverified_context

except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

MANIFEST = {
    "id": "vijai",
    "version": "1.0.2",
    "name": "vijai",
    "description": "Sample addon made with Flask providing a few public domain movies",
    "types": ["movie"],
    "catalogs": [
        {"type": "movie", "name": "tamilgun_HD_movies", "id": "tamilgun_HD_movies"},
        {"type": "movie", "name": "movierulz_tamil", "id": "movierulz_tamil"},
    ],
    "resources": [
        "catalog",
        "stream",
        "meta"
        # The meta call will be invoked only for series with ID starting with hpy
        # {'name': "meta", 'types': ["movie"], 'idPrefixes': ["tamilgun_HD_movies","tamilgun_New_movies"]},
        # {'name': 'stream', 'types': ["movie"], 'idPrefixes': ["tamilgun_HD_movies","tamilgun_New_movies"]}
    ],
}

def getdatacontent(url, reg):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(url)
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    data = []
    try:
        r = opener.open(req)
        html = r.read().decode("utf-8")
        data = re.compile(reg).findall(html)
        print(data)
        return data
    except:
        print("Error getting data content---------------*-*-*-*-")


# def gethtmlcontent(url):
#     try:
#         _create_unverified_https_context = ssl._create_unverified_context

#     except AttributeError:
#         pass
#     else:
#         ssl._create_default_https_context =_create_unverified_https_context
#     proxy_handler = urllib2.ProxyHandler({})
#     opener = urllib2.build_opener(proxy_handler)
#     req = urllib2.Request(url)
#     opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#     r = opener.open(req)
#     html = r.read().decode('utf-8')
#     return html


def gethtmlcontent(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
    }
    response = requests.get(url, headers=headers, verify=False)
    result = response.text
    return result


def gettamilgunstreamurl(url):
    movielist = []
    temp = {}
    reg = '<(iframe|IFRAME)(\\s|.*?)(src|SRC)=\\"(?P<streamurl>.*?)\\"|onclick=\\"window\\.open\\(\\"(?P<streamurl1>.*?)\\"|sources:\\s+\\[{\\"file\\":\\"(?P<streamurl2>.*?)\\"}\\]'
    urls = getdatacontent(url, reg)
    for url in urls[0]:
        if "embed1.tamildbox" in url:
            movieurl = embedtamilgun.resolve_embedtamilgun(url)
            try:
                if movieurl:
                    temp["title"] = "embed1.tamildbox"
                    temp["url"] = movieurl
                    movielist.append(temp)
                else:
                    temp["url"] = ""
            except:
                pass
        elif "cdn.jwplayer" in url:
            movieurl = embedtamilgun.resolve_cdnjwplayer(url)
            try:
                if movieurl:
                    temp["title"] = "cdn.jwplayer"
                    temp["url"] = movieurl
                    movielist.append(temp)
                else:
                    temp["url"] = ""
            except:
                pass
        elif "myfeminist" in url:
            movieurl = myfeminist.resolve_myfeminist(url)
            try:
                if movieurl:
                    temp["title"] = "myfeminist"
                    temp["url"] = movieurl
                    movielist.append(temp)
                else:
                    temp["url"] = ""
            except:
                pass
    return movielist


def getmovierulzstreamurl(url):
    movielist = []
    temp = {}
    temp["url"] = ""
    reg = '<p><strong>(.*?)<\/strong><br \/>\s+<a href="(.*?)"'
    urls = getdatacontent(url, reg)
    if urls:
        for url in urls:
            if "downscrs" in url[1]:
                movieurl = downscrs.resolve_downscrs(url[1])
                try:
                    if movieurl:
                        temp["title"] = "downscrs"
                        temp["url"] = movieurl
                        movielist.append(temp)
                    else:
                        temp["url"] = ""
                        movielist.append(temp)
                except:
                    pass
            elif "downsrs12346" in url[1]:
                movieurl = downscrs.resolve_downscrs(url[1])
                try:
                    if movieurl:
                        temp["title"] = "downsrs"
                        temp["url"] = movieurl
                        movielist.append(temp)
                    else:
                        temp["url"] = ""
                        movielist.append(temp)
                except:
                    pass
    return movielist


def appendtamilgundatatocatalog(data, id):
    CATALOG[id] = {}
    CATALOG[id]["movie"] = []
    for item in data:
        temp = {}
        temp["poster"] = item[0]
        temp["name"] = item[1]
        temp["id"] = id + "_-" + item[1]
        CATALOG[id]["movie"].append(temp)
        url = item[2]
        stream_url = gettamilgunstreamurl(url)
        STREAMS["movie"].update({temp["id"]: stream_url})


def appendmovierulzdatatocatalog(data, id):
    CATALOG[id] = {}
    CATALOG[id]["movie"] = []
    for item in data:
        temp = {}
        poster = item[2]
        poster = poster.split('/')
        poster = poster[-1:]
        posterlink = "https://ww16.moviesrulz.net/uploads/"+poster[0]+'?1'
        temp["poster"] = posterlink
        temp["name"] = item[1]
        temp["id"] = id + "_-" + item[1]
        CATALOG[id]["movie"].append(temp)
        url = item[0]
        stream_url = getmovierulzstreamurl(url)
        STREAMS["movie"].update({temp["id"]: stream_url})


#### Main Program Starts Here #############
global STREAMS
global CATALOG
CATALOG = {}
STREAMS = {}
STREAMS["movie"] = {}
# TamilGUn site Part Starts Here -------------------------------------------------------------------
url = "http://tamilgun.com"
r = requests.get(url)
url = r.url
url = url.split("/")
url = "http://" + url[2]
tamilgun_HD_movie = url + "/categories/hd-movies/"
reg = '<img src=" (.*?) " alt="(.*?)" \/>\s+<div class="rocky-effect">\s+<a href="(.*?)" >'
try:
    data = getdatacontent(tamilgun_HD_movie, reg)
    appendtamilgundatatocatalog(data, "tamilgun_HD_movies")
except:
    pass
##TamilGUn site Part Ends Here -------------------------------------------------------------------
##Movierulz site Part Starts Here-----------------------------------------------------------------
data = ""
url = "https://ww2.7movierulz.pe"
url = url + "/category/tamil-movie/"
reg = '<a href="(.*?)"\stitle="(.*?)">\s*<img width="\d+" height="\d+" src="(.*?)"'
try:
    data = getdatacontent(url, reg)
    data = data[2:]
    appendmovierulzdatatocatalog(data, "movierulz_tamil")
except:
    pass

##Movierulz site Part Ends Here-------------------------------------------------------------------


app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    return resp


@app.route("/manifest.json")
def addon_manifest():
    return respond_with(MANIFEST)


@app.route("/stream/<type>/<id>.json")
def addon_stream(type, id):
    if type not in MANIFEST["types"]:
        abort(404)

    streams = {"streams": []}
    if type in STREAMS and id in STREAMS[type]:
        streams["streams"] = STREAMS[type][id]
    return respond_with(streams)


@app.route("/catalog/<type>/<id>.json")
def addon_catalog(type, id):
    if type not in MANIFEST["types"]:
        abort(404)

    catalog = CATALOG[id][type] if type in CATALOG[id] else []
    metaPreviews = {
        "metas": [
            {
                "id": item["id"],
                "type": type,
                "name": item["name"],
                "poster": item["poster"],
                "director": "Links",
                "background": item["poster"],
                "logo": item["poster"],
            }
            for item in catalog
        ]
    }
    return respond_with(metaPreviews)


OPTIONAL_META = [
    "posterShape",
    "background",
    "logo",
    "videos",
    "description",
    "releaseInfo",
    "imdbRating",
    "director",
    "cast",
    "dvdRelease",
    "released",
    "inTheaters",
    "certification",
    "runtime",
    "language",
    "country",
    "awards",
    "website",
    "isPeered",
]


@app.route("/meta/<type>/<id>.json")
def addon_meta(type, id):
    if type not in MANIFEST["types"]:
        abort(404)

    def mk_item(item):
        meta = dict((key, item[key]) for key in item.keys() if key in OPTIONAL_META)
        meta["id"] = item["id"]
        meta["type"] = type
        meta["name"] = item["name"]
        meta["poster"] = item["poster"]
        meta["director"] = "Links:"
        meta["background"] = item["poster"]
        meta["logo"] = item["poster"]
        return meta

    name = id.split("_-")
    name = name[0]
    meta = {
        "meta": next(
            (mk_item(item) for item in CATALOG[name][type] if item["id"] == id), None
        )
    }

    return respond_with(meta)


if __name__ == "__main__":
    app.run(debug=True)

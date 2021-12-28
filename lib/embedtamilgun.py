import urllib.request, urllib.error, urllib.parse,re,urllib.request,urllib.parse,urllib.error,requests

def getcontent(url):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read().decode('utf-8')
    return html

def getcontenttamildbox(url):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'DNT': '1',
        'Accept': '*/*',
        'Origin': 'https://embed1.tamildbox.tips',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://embed1.tamildbox.tips/',
        'Accept-Language': 'en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7,fr-FR;q=0.6,fr;q=0.5',
    }
    response = requests.get(url, headers=headers)
    return response

def getdatacontent(url,reg):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read().decode('utf-8')
    data = re.compile(reg).findall(html)
    return data

def resolve_embedtamilgun(url):
    reg ='var\slink_play\s=\s+\[\{"file":\"(.*?)\"'
    url = getdatacontent(url,reg)
    if url:
        return url[0]
    else:
        return None

def resolve_cdnjwplayer(url):
    reg = '<meta name="twitter:player:stream" content=\"(.*?)\">'
    url = getdatacontent(url,reg)
    if url:
        return url[0]
    else:
        return None

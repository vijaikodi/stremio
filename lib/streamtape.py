import urllib.request, urllib.error, urllib.parse,re,urllib.request,urllib.parse,urllib.error,requests

def getdatacontent_dict(url,reg):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read().decode('utf-8')
    r = re.compile(reg)
    data = [m.groupdict() for m in r.finditer(html)]
    return data
def getdatacontent(url,reg):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read().decode('utf-8')
    data = re.compile(reg).findall(html)
    return data

def getcontent(url):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read().decode('utf-8')
    return html

def get_redirect_url(url, headers={}):
    request = urllib.request.Request(url, headers=headers)
    request.get_method = lambda: 'HEAD'
    response = urllib.request.urlopen(request)
    return response.geturl()

# def resolve_streamtape(url):
#     reg ='<iframe src="(.*?)"'
#     url = getdatacontent(url,reg)
#     url = url[0]
#     # reg = '"videolink"[^>]+>([^<]+)'
#     # url = getdatacontent(url,reg)
#     # url = url[0]
#     # url = 'http:'+url
#     movieurl = urlresolver.HostedMediaFile(url)
#     movieurl = movieurl.resolve()
#     return movieurl

def resolve_streamtape(url):
    reg = "id=(?P<id>.*?)&expires=(?P<expires>.*?)&ip=(?P<ip>.*?)&token=(?P<token>.*?)\'"
    data = getdatacontent_dict(url,reg)
    data = data[0]
    headers = {
        'authority': 'streamtape.to',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'video',
        'referer': url,
        'accept-language': 'en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7,fr-FR;q=0.6,fr;q=0.5',
        'range': 'bytes=0-',
    }

    params = (
        ('id', data['id']),
        ('expires', data['expires']),
        ('ip', data['ip']),
        ('token', data['token']),
        ('stream', '1'),
    )

    url = "https://streamtape.to/get_video?id="+data['id']+"&expires="+data['expires']+"&ip="+data['ip']+"&token="+data['token']+"&stream=1"
    url = get_redirect_url(url,headers=headers)
    return url

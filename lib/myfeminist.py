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

def resolve_myfeminist(url):
    reg = 'sources:\s+\[{file:\"(.*?)\"'
    link = getdatacontent(url,reg)
    return link[0]

import urllib.request, urllib.error, urllib.parse, re, urllib.request, urllib.parse, urllib.error, requests
from lib import streamtape


def getdatacontent_dict(url, reg):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    r = opener.open(req)
    html = r.read().decode("utf-8")
    r = re.compile(reg)
    data = [m.groupdict() for m in r.finditer(html)]
    return data


def getdatacontent(url, reg):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    r = opener.open(req)
    html = r.read().decode("utf-8")
    data = re.compile(reg).findall(html)
    return data


def getcontent(url):
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url)
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    r = opener.open(req)
    html = r.read().decode("utf-8")
    return html


def get_redirect_url(url, headers={}):
    request = urllib.request.Request(url, headers=headers)
    request.get_method = lambda: "HEAD"
    response = urllib.request.urlopen(request)
    return response.geturl()


def resolve_downscrs(url):
    reg = '<iframe\sloading="lazy"\ssrc="(.*?)"'
    link = getdatacontent(url, reg)
    link = link[0]
    if link:
        if "ncdnstm" in link:
            link = link.split("/")
            link = link[-1]
            url = "https://ncdnstm.com/api/source/" + link
            x = requests.post(url)
            x = x.text
            reg = '{"file":"(.*)"'
            link = re.compile(reg).findall(x)
            link = link[0]
            link = link.replace("\\", "")
            return link

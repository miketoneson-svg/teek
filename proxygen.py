import requests
from lxml.html import fromstring

PROXY_CACHE = None


def get_proxies():
    global PROXY_CACHE

    if PROXY_CACHE is not None:
        return PROXY_CACHE

    url = "https://sslproxies.org/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return set()

    parser = fromstring(response.text)
    proxies = set()
    for row in parser.xpath('//tbody/tr')[:10]:
        if row.xpath('.//td[7][contains(text(),"yes")]'):
            ip = row.xpath('.//td[1]/text()')
            port = row.xpath('.//td[2]/text()')
            if ip and port:
                proxies.add(f"{ip[0]}:{port[0]}")

    PROXY_CACHE = proxies
    return proxies

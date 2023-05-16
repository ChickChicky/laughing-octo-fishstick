import requests
import urllib.parse
import re
import threading

urls:list[str] = []

def searchURL(query:str) -> str:
    """
    Generates a search URL query
    """
    return f'https://www.google.com/search?q={urllib.parse.quote(query)}'

def URLfn(url:str) -> bool:
    """
    Checks whether the URL has already been explored and adds it to the list if it is not the case
    """
    if url in urls:
        return True
    else:
        urls.append(url)
        return False

# def URLfn(url:str) -> bool:
#     """
#     Checks whether the URL has already been explored and adds it to the list if it is not the case
#     """
#     if hash(url) in urls:
#         return True
#     else:
#         urls.append(hash(url))
#         return False

tmp:list[str] = []

if True:
    url = searchURL(input('Search query: '))
    print(f'\x1b[A\x1b[G\x1b[KStart URL: \x1b[32m{url}\x1b[39m')
    tmp.append(url)
    
def reqT(url:str,n_tmp:list[str]):
    try:
        req = requests.get(url)
        content = req.content.decode(errors='ignore')
        n_tmp.extend(filter(lambda u:not URLfn(u),re.findall("http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]|[$\-_@.&+/]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",content)))
    except: pass

loops = 0
while True:
    e = "" if loops==0 else "\x1b[2A\x1b[G\x1b[J"
    print(f'{e}Explored URLs: \x1b[33m{len(urls)}\x1b[39m\nURLs to explore: \x1b[33m{len(tmp)}\x1b[39m')
    n_tmp = []
    threads:list[threading.Thread] = []
    for url in tmp:
        t = threading.Thread(target=reqT,args=(url,n_tmp))
        t.start()
        threads.append(t)
    for t in threads: t.join()
    tmp,n_tmp = n_tmp,tmp
    loops = loops+1
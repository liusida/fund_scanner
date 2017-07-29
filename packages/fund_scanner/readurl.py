import os
import urllib.request
import shutil
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

def copy_from_url_to_file(url, tmpfile):
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(tmpfile, 'wb') as local_fo:
            shutil.copyfileobj(response, local_fo)
        
def read_from_file(tmpfile):
    with open(tmpfile, 'rb') as local_fo:
        body = local_fo.read().decode('utf-8')
    return body

def read_from_url(url, tmpfile=''):
    if tmpfile=='':
        directory = '/tmp/fund_scanner/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        tmpfile = os.path.join(directory, 'read_from_url_'+str(time.time())+'.tmp')
        
    copy_from_url_to_file(url, tmpfile)
    return read_from_file(tmpfile)


def simple_read_from_url(url):
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

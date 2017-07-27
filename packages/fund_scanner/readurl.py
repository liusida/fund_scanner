import os
import urllib.request
import shutil
import time


def copy_from_url_to_file(url, tmpfile):
    remote_fo = urllib.request.urlopen(url)
    with open(tmpfile, 'wb') as local_fo:
        shutil.copyfileobj(remote_fo, local_fo)
        
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
    return urllib.request.urlopen(url).read().decode('utf-8')

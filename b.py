from multiprocessing import Pool
import os, re, time, random
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlretrieve
import datetime
import redis
import uuid

def urllib_download():
    for index in range(0, 9999999):
        id = r.lpop('list')
        print(id)
        if id:
            info = r.hgetall(id)
            print(info)
            urlretrieve(info['remote_url'], info['local_url'])
            print('successful')
        else:
            print('done')
            break


if __name__=='__main__':
    #初始化
    url = 'https://www.meitulu.com/'
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    classify = []  #大分类url和名称
    all_child_page = [] #大分类下全部带分页页面及名称

    #get_url()
    urllib_download()

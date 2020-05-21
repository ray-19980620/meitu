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
        if id:
            info = r.hgetall(id)
            print(info)
            urlretrieve(info['remote_url'], info['local_url'])
            print('successful')
        else:
            print('done')

# #获取分类名/url 拼装dict
def get_url():
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    tag_list = soup.find(id = 'tag_ul')
    tag_a = tag_list.find_all('a')
    for a_index,a_item in enumerate(tag_a):
        d = {'name': a_item.string, 'url': a_item.get('href')}
        classify.append(d)

    for index, tag in enumerate(classify):
        #if index > 0:
            #break

        html_doc = urllib.request.urlopen(tag['url'])
        soup = BeautifulSoup(html_doc, 'html.parser')
        page_div = soup.find(id = 'pages')
        a_dic = []
        #获取分页总页数a_dic[-2]
        for page_a in page_div.find_all('a'):
            a_dic.append(page_a.string)

        if len(a_dic) == 0:
            continue

        for page in range(1, int(a_dic[-2]) + 1):
            if page == 1:
                classify_page_url = tag['url']
            else:    
                classify_page_url = tag['url'] + str(page) + '.html'

            all_child_page.append({'name': tag['name'], 'url': classify_page_url, 'page': page})
            #print(classify_page_url)
        
        for page_index, page_item in enumerate(all_child_page):
            #if page_index > 2:
                #break

            html_doc_child = urllib.request.urlopen(page_item['url'])
            soup_child = BeautifulSoup(html_doc_child, 'html.parser')

            page_div_child = soup_child.find(id = 'pages')

            img_ul = soup.find(name = 'ul', attrs={'class','img'}).find_all('img')
            for img_index, img_item in enumerate(img_ul):
                dir_name = img_item.get('alt')
                base_url = img_item.parent.get('href').replace('.html', '')
                html_doc = urllib.request.urlopen(img_item.parent.get('href'))
                soup = BeautifulSoup(html_doc, 'html.parser')
                page_div = soup.find(id = 'pages')
                b_dic = []
                for page_a in page_div.find_all('a'):
                    b_dic.append(page_a.string)

                if len(b_dic) == 0:
                    continue

                for page in range(1, int(b_dic[-2]) + 1):
                    if page == 1:
                        classify_page_url_child = base_url + '.html'
                    else:
                        classify_page_url_child = base_url + '_' + str(page) + '.html'

                    print(classify_page_url_child)
                    html_doc = urllib.request.urlopen(classify_page_url_child)
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    file_parent_name = re.sub(r'[\s*]\d*|', '', soup.find('h1').string.replace('/', ''))
                    dir = 'e:/meitu/img/' + tag['name'] + '/' + file_parent_name
                    print(dir)

                    file_exist = os.path.exists(dir)
                    if page == 1 and not file_exist:
                        os.makedirs(dir)
                        
                    img = soup.find('center').find_all('img')
                    for img_index, img_item in enumerate(img):
                        #print('获取到了地址')
                        img_src = img_item.get('src')
                        (file, ext) = os.path.splitext(img_src)
                        id = uuid.uuid1()
                        _file = dir + '/' + str(id) + ext
                        r.lpush('list', id)
                        r.hmset(id, {'remote_url': img_src, 'local_url': _file})
                        print('push ok')
                    #urllib_download(img_src, _file)



if __name__=='__main__':
    #初始化
    url = 'https://www.meitulu.com/'
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    classify = []  #大分类url和名称
    all_child_page = [] #大分类下全部带分页页面及名称

    get_url()
    urllib_download()

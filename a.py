import os,re
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlretrieve
import datetime

def urllib_download(remote_url, local_url):
    urlretrieve(remote_url, local_url)  


# def get_page_img_info(img_page):
#     dir = 'd:/meitu/album/img/' + img_page['type'] + '/' + img_page['name']
#     if not os.path.exists(dir):
#         os.makedirs(dir)
    
#     html_doc = urllib.request.urlopen(img_page['url'])
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     img = soup.find('center').find_all('img')
#     for img_index, img_item in enumerate(img):
#         img_src = img_item.get('src')
#         (file, ext) = os.path.splitext(img_src)
#         _file = dir + '/' + str(img_index) + ext
#         if not os.path.exists(_file):
#             urllib_download(img_src, _file)
#             print('download successful!!!')

#初始化
url = 'https://www.meitulu.com/'
classify = []  #大分类url和名称
all_child_page = [] #大分类下全部带分页页面及名称


#获取分类名/url 拼装dict
html_doc = urllib.request.urlopen(url)
soup = BeautifulSoup(html_doc, 'html.parser')
tag_list = soup.find(id = 'tag_ul')
tag_a = tag_list.find_all('a')
for a_index,a_item in enumerate(tag_a):
    d = {'name': a_item.string, 'url': a_item.get('href')}
    classify.append(d)

for index, tag in enumerate(classify):
    # if index > 0:
    #     break

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
        # if page_index > 2:
        #     break

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
                #print('文件夹存在否')
                if not os.path.exists(dir):
                    #print('不存在')
                    os.makedirs(dir)

                #print('存在')
                img = soup.find('center').find_all('img')
                for img_index, img_item in enumerate(img):
                    #print('获取到了地址')
                    img_src = img_item.get('src')
                    (file, ext) = os.path.splitext(img_src)
                    _file = dir + '/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
                    #if not os.path.exists(_file):
                    #print('ready')
                    urllib_download(img_src, _file)
                    print('download successful!!!')

        #print(album_page)

    #print(all_child_page)





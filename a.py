from bs4 import BeautifulSoup
import urllib.request

#初始化
url = 'https://www.meitulu.com/'
classify = []  #大分类url和名称
all_child_page = [] #大分类下全部带分页页面及名称
album_page = [] #全部图集url


#获取分类名/url 拼装dict
html_doc = urllib.request.urlopen(url)
soup = BeautifulSoup(html_doc, 'html.parser')
tag_list = soup.find(id = 'tag_ul')
tag_a = tag_list.find_all('a')
for a_index,a_item in enumerate(tag_a):
    d = {'name': a_item.string, 'url': a_item.get('href')}
    classify.append(d)

for index, tag in enumerate(classify):
    if index > 0:
        break

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
        if index > 0:
            break

        html_doc = urllib.request.urlopen(page_item['url'])
        soup = BeautifulSoup(html_doc, 'html.parser')
        img_ul = soup.find(name = 'ul', attrs={'class','img'}).find_all('li')
        for img_index, img_item in enumerate(img_ul):
            pass

    #print(all_child_page)


def get_page_img_info(url):
    pass


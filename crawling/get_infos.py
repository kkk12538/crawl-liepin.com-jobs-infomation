import requests
from lxml import etree
import re
import jieba
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib as mpl

url = 'https://www.liepin.com/job/1931332745.shtml'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
page_text = requests.get(url=url, headers=headers).text
tree = etree.HTML(page_text)

#   获取所有职位描述
infos = tree.xpath('//div[@class="content content-word"][1]/text()')
for i in range(len(infos)):
    if infos[i] != 'b.任职要求':
        infos[i] = ''
    else:
        break
infos = ''.join(infos)

#   去除特殊字符和字母
infos = ' '.join(re.findall('[\u4e00-\u9fa50-9]+', infos))
print('任职要求：')
print(infos)
#   设置中文字体
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
#   绘制词云图
keywords = ' '.join(jieba.lcut(infos))
image= Image.open('pictures/ball.jpg')            #背景图片
graph = np.array(image)
wc = WordCloud(font_path='msyh.ttc',
    background_color=None, mode='RGBA',
    max_words=200,         #设置最大词数
    mask=graph,             #设置背景图片
    max_font_size = 150,  #设置字体最大值
    random_state = 50,   #有多少种随机状态
    scale=1)
word_cloud = wc.generate(keywords)
plt.imshow(wc)
plt.axis("off")
plt.savefig('./pictures/wordcloud.png')
plt.show()


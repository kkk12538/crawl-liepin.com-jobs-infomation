import requests
from lxml import etree
from multiprocessing.dummy import Pool
jobs=['数据挖掘','图像算法工程师','java后端','互联网产品经理']

def getData(job):
    #   北京 上海 广州 深圳  杭州 武汉
    city_numbers=['010','020','050020','050090','070020','170020']
    # for job in jobs:
    urls=[]
    for city in city_numbers:
        for i in range(3):
            url='https://www.liepin.com/zhaopin/?dqs='+city+'&pageSize=40&d_curPage='+str(i)+'&key='+job
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
            page_text=requests.get(url=url,headers=headers).text
            tree=etree.HTML(page_text)
            li_list=tree.xpath('//ul[@class="sojob-list"]/li')
            #   遍历所有li
            for li in li_list:
                detail_url=li.xpath('./div/div/h3/a/@href')[0]
                if str(detail_url).split('/')[0]!='https:':
                    detail_url='https://www.liepin.com'+detail_url
                urls.append(detail_url)
    print(job + '职位信息爬取成功！')
    file_name=job+'.txt'
    with open(file_name,'w',encoding='utf8') as fp:
        for i in urls:
            fp.writelines(i)
            fp.write("\n")

#   使用多线程进行爬取
pool=Pool(4)
pool.map(getData,jobs)
pool.close()
pool.join()

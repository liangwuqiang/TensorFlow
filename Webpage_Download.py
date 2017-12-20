# -*- coding: utf-8 -*-
"""
功能：
下载指定网页中的文章内容
使用方法：
在main函数中修改urls中的网址，运行（如果没有对应的标题、内容提取关键字，需要添加）
"""
from urllib import request
from bs4 import BeautifulSoup
import re
import os
import codecs


class WebPageDownload:  # 专门用于提取网页中文章内容，包含标题、内容和图片

    def __init__(self, url, title_key, content_key):
        self.url = url  # 网址
        self.titleKey = title_key  # 文章标题提取关键字
        self.contentKey = content_key  # 文章内容提取关键字
        self.title = ''  # 文章标题
        self.content = ''  # 文章内容

    def url_to_html(self):  # 通过网址取得整个网页的内容
        req = request.Request(self.url)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html

    def extract_from_soup(self, html):  # 提取标题和文章内容
        soup = BeautifulSoup(html, 'html.parser')
        self.title = soup.select(self.titleKey)[0].text.strip()
        print(self.title)  # 用于测试
        self.content = soup.select(self.contentKey)[0]

    @staticmethod
    def md5(string):  # 将图片网址转成哈希码
        import hashlib
        if not isinstance(string, str):
            string = str(string)
        md5 = hashlib.md5()
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()

    def download_images(self):  # 下载文章中的图片
        content = str(self.content)
        pattern = '<img .*?src=\"(.*?)\"'
        re_image = re.compile(pattern)
        for imageUrl in re_image.findall(content):
            if not os.path.exists('output'):
                os.mkdir('output')
            if not os.path.exists('output/images'):
                os.mkdir('output/images')
            filename = 'images/' + self.md5(imageUrl) + os.path.splitext(imageUrl)[-1]
            try:
                request.urlretrieve(imageUrl, 'output/' + filename)
                pass
            except Exception as e:
                print('图片出错', e)
            else:
                content = content.replace(imageUrl, filename)
            print('输出图像：' + imageUrl)
        self.content = content

    def output_html(self):  # 输出html文件
        html_template = """<!DOCTYPE html>
            <html><head><meta charset="UTF-8">
            </head><body>
            <p><a href="{origin}">原文链接</a></p>
            <p><center><h1>{title}</h1></center></p>
                {content}
            </body></html>"""
        html = html_template.format(origin=self.url, title=self.title, content=self.content)
        filename = "output/" + str(self.title) + ".html"
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write(html)

    def run(self):  # 程序执行步骤
        html = self.url_to_html()  # 第一步：通过网址获取整个网页
        # print(html)
        self.extract_from_soup(html)  # 第二步：从网页中提取文章
        self.download_images()  # 第三步：下载文章中的图片，修改图片的超链接
        self.output_html()  # 构建HTML文件，并存盘输出


def dealer(urls):  # 网址群拆分，根据网址自动获得对应的提取关键字
    for url in urls.split('\n'):
        url = url.strip()
        if url:
            if 'blog.jobbole.com' in url:  # 伯乐在线 http://blog.jobbole.com/105602/
                title_key = '.entry-header'
                content_key = '.entry'
            elif 'blog.csdn.net' in url:  # csdn
                title_key = '.link_title'
                content_key = '#article_content'
            elif 'www.codingpy.com' in url:  # 编程派网址
                title_key = '.header h1'
                content_key = '.article-content'
            elif 'www.infoq.com' in url:  # InfoQ http://www.infoq.com/cn/articles/introduction-of-tensorflow-part01
                title_key = '.title_canvas'
                content_key = '.text_info_article'
            else:
                title_key = ''
                content_key = ''

            if title_key and content_key:
                print(url)
                my_download = WebPageDownload(url, title_key, content_key)
                my_download.run()
                pass
            break  # 只要下载第一项


def main():
    print('== 程序开始运行 ==')
    urls = """
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part01
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part02
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part03
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part4
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part05
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part06
        http://www.infoq.com/cn/articles/introduction-of-tensorflow-part07
        """
    dealer(urls)
    print('== 程序全部运行完毕 ==')


if __name__ == '__main__':
    main()

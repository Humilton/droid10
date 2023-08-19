#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys, os
import pytz
from datetime import datetime
import urllib.request
from urllib.parse import urlparse,unquote
import choice
import cgi
import re
import traceback
from pyquery import PyQuery as pq
from markdownify import MarkdownConverter
from multiprocessing import Pool

def openImgUrl(src):
    fname = None
    response = None
    if src and "http" in src:
        target = os.path.basename(urlparse(src).path)
        fname = "imgs/%s_%s" % ("vjob" ,target)
        cnt = 1
        while os.path.isfile(fname) or os.path.isfile("/work/work/img.vjob.top/" + fname):
            if src in saved_img_src:
                return fname,response
            fname = "imgs/%s_%d_%s" % ("vjob" ,cnt, target)
            cnt = cnt + 1
        try:
            request = urllib.request.Request(src, headers=header)
            response = urllib.request.urlopen(request, timeout=30)
            saved_img_src.append(src)
        except:
            print(traceback.format_exc(), file=sys.stderr)
            pass
    return fname,response

saved_img_src = []
class ImageBlockConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        #return super().convert_img(el, text, convert_as_inline) + '\n\n'
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        fname,response = openImgUrl(src)
        if fname:  # download and save
            if response:
                data = response.read()
                file = open(fname , "wb")
                file.write(data)
                file.close()
            src = "http://i.vjob.top:8000/" + fname
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if convert_as_inline:
            return alt
        return '![%s](%s%s)\n' % (alt, src, title_part)

# Create shorthand method for conversion
def md(html, **options):
    options['escape_underscores'] = False
    options['strip'] = ["style"]
    return ImageBlockConverter(**options).convert(html)

user_agent = [
# 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/56.0.2924.87 safari/537.36',
# 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
# 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
]
#header = {'user-agent': choice(user_agent)}
#header = {'user-agent': user_agent[0], 'dnt':'1', 'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'}
header = {'user-agent': user_agent[0]}
#header2 = {'user-agent': user_agent[0], 'dnt':'1', 'accept-language': 'zh-TW;q=0.9,en-US;q=0.8,en;q=0.6'}
#proxy_host = "127.0.0.1:7890"

class Utils:
    @staticmethod
    def getDoc(site):
        return Utils.getDocWithEnc(site)
        
    @staticmethod
    def getDocWithEnc(site):
        try:
            if site.startswith('http'):
                request = urllib.request.Request(site, headers=header)
                r = urllib.request.urlopen(request, timeout=30) 
                html = r.read()
                #cCharset = r.headers.get_content_charset()
                ##print(site + " : " + cCharset)
                #if cCharset:
                #    html = html.decode(cCharset)
                doc = pq(html)
                doc.make_links_absolute(site)
            else:
                doc = pq(filename=site)
        except:
            print(traceback.format_exc()[:-1], file=sys.stderr)
            return None
        return doc

__tz__ = pytz.timezone('Asia/Shanghai')
class DateUtil:
    @staticmethod
    def getDay():
        ct = datetime.now(tz=__tz__)
        return ct.strftime(u"%Y%m%d")
        
    @staticmethod
    def getTime():
        ct = datetime.now(tz=__tz__)
        return ct.strftime(u"%Y-%m-%d %H:%M:%S")
    
filterMap = {
".post-title" : ".post-content",
".entry-title" : ".entry-content",
".entry-title" : ".entry",
".article-header" : ".article_content",
".entry-header" : ".entry-content",
".page-header" : ".entry-content",
#".blog_title h3" : "#blog_content",
"#question-header" : "#mainbar",
".title" : ".content",
".title" : ".article-content-wrap",
".topic-title" : ".content",
".page-title" : ".field--body",
".doc-title":"#reader-container"
}

class pageSpider():
    def __init__(self, postFilter="article"):
        self.postFilter = postFilter  # Filter Post for a page
        self.spiderPageDetails = md  # fuc to spider detail
    
    def filter(self, href):
        return True

    def spiderPage(self, site):
        # if "iteye.com" in site or "zyxware.com" in site or "element14.com" in site or "findhao.net" in site:
        if "stackexchange.com" in site or "askubuntu.com" in site or "htpcguides.com" in site:
            return [None, None]
        doc = Utils.getDoc(site)
        if not doc:
            return [None, None]
        if doc(".post-title") and doc(".post-content"):
            title = doc(".post-title").text()
            post = doc(".post-content")
        elif doc(".post-title") and doc(".post-body"):
            title = doc(".post-title").text()
            post = doc(".post-body")
        elif doc(".postTitle") and doc(".postBody"):
            title = doc(".postTitle").text()
            post = doc(".postBody")
        elif doc(".entry-title") and doc(".entry-content"):
            title = doc(".entry-title").text()
            post = doc(".entry-content")
        elif doc(".entry-title") and doc(".entry"):
            title = doc(".entry-title").text()
            post = doc(".entry")
        elif doc(".article-header") and doc(".article_content"):
            title = doc(".article-header").text()
            post = doc(".article_content")
        elif doc(".entry-header") and doc(".entry-content"):
            title = doc(".entry-header").text()
            post = doc(".entry-content")
        elif doc(".page-header") and doc(".entry-content"):
            title = doc(".page-header").text()
            post = doc(".entry-content")
        elif doc(".blog_title") and doc("#blog_content"):
            title = doc(".blog_itle").text()
            post = doc("#blog_content")
        elif doc("#question-header") and doc("#mainbar"):
            title = doc("#question-header").text()
            post = doc("#mainbar")
        elif doc(".title") and doc(".content"):
            title = doc(".title").text()
            post = doc(".content")
        elif doc(".title") and doc(".article-content-wrap"):
            title = doc(".title").text()
            post = doc(".article-content-wrap")
        elif doc(".title") and doc(".entry"):
            title = doc(".title").text()
            post = doc(".entry")
        elif doc(".topic-title") and doc(".content"):
            title = doc(".topic-title").text()
            post = doc(".content")
        elif "https://www.digitalocean.com/" in site:
            title = doc("div.HeadingStyles__StyledH1-sc-kkk1io-0").text()
            post = doc("div.MarkdownStyles__StyledMarkdown-sc-bjjo5d-0")
        elif doc("#docs-body"):
            title = doc('title').text()
            post = doc("#docs-body")
        elif doc(".page-title") and doc(".field--body"):
            title = doc('.page-title').text()
            post = doc(".field--body")
        elif doc(".doc-title") and doc("#reader-container"):
            title = doc('.doc-title').text()
            post = doc("#reader-container")
        elif doc(".article-title a") and doc(".paragraphsContainer"):
            title = doc('.article-title a').text()
            post = doc(".paragraphsContainer")
        else:
            if doc("h1"):
                title = doc("h1").text()
            else:
                title = doc('title').text()
            if doc(".article-content"):
                post = doc(".article-content")
            elif doc("#content"):
                post = doc("#content")
            elif doc(".markdown"):
                post = doc(".markdown")
            elif doc(".article-main"):
                post = doc(".article-main")
            elif doc("#js_content"):
                post = doc("#js_content")
            else:
                post = doc("article")
        if not post:
            print("doc : " + str(doc))
        if "charry.org" in site:
            post = doc("body")
        elif "gbhackers.com" in site:
            post = doc(".td-post-content")
        elif "openwrt.org" in site:
            post = doc("#dokuwiki__content")
        detail= self.spiderPageDetails(post.html())

        if len(title) > 100 or len(title) < 2:
            title = doc('title').text()
        if "-CSDN博客" in title:
            idx = title.rindex("-")
            title = title[0:idx]
            if "_" in title:
                idx = title.rindex("_")
                title = title[0:idx]
        if " -" in title:
            idx = title.rindex(" -")
            title = title[0:idx]
        if "\n" in title:
            idx = title.index("\n")
            title = title[0:idx]
        if "|" in title:
            idx = title.index("|")
            title = title[0:idx]
        if ":" in title:
            if "MySQL" in title:
                idx = title.rindex(":")
                title = re.sub("[\d\.]+","", title[idx+1:]).strip()
            elif ": " in title:
                title = title.replace(": ", ":")
            elif " :" in title:
                title = title.replace(" :", ":")
        return [title.strip(), detail]

def getFileName(title):
    fname = title
    if "/" in fname:
        fname = fname.replace("/", "_")
    if "\\" in fname:
        fname = fname.replace("\\", "_")
    return fname + ".md"

def runSpider(page):
    if "#" in page and page.index("#") == 0:
        return
    try:
        #spider = pageSpider("#content_views")
        spider = pageSpider()
        [title, detail] = spider.spiderPage(page)
        if title:
            f = open(getFileName(title), "w")
            print("## ", title, "\n\n", detail, file=f)
            page = unquote(page)
            print("\n原文链接： [" + page + "](", page + ")", file=f)
            f.close()
            print( "Spidering page : " + page + " @ " + (DateUtil.getTime()))
        else:
            print( "Spidering page : " + page + " fail --- with none title @ " + (DateUtil.getTime()) + "\n")
    except Exception as e:
        print( "Spidering page : " + page + " @ " + (DateUtil.getTime()), file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", help="get url")
    parser.add_argument("-src", help="read many links from src")
    args = parser.parse_args()
    
    page = args.url
    src = args.src
    if page:
        runSpider(page)
    elif src:
        file = open(src,"r")
        pages = file.read()
        file.close()
        multiSpider(pages.split("\n"))
    else:
        parser.print_help()
    
def multiSpider(pages):
    # pages=[
    # "https://yian.me/blog/cs/install-chromium-and-google-pinyin-on-raspberry-pi-2.html",
    # "https://www.hscbook.com/article/raspberrypi-audio/",
    # "http://logan.tw/posts/2015/11/15/autossh-and-systemd-service/",
    # "https://askubuntu.com/questions/19320/how-to-enable-or-disable-services",
    # #"https://github.com/xdtianyu/scripts/tree/master/lets-encrypt",
    # "http://bolg.malu.me/html/2011/1809.html",
    # "https://askubuntu.com/questions/299792/why-is-the-command-in-etc-rc-local-not-executed-during-startup",
    # "https://blog.longwin.com.tw/2010/10/mysql-upgrade-cmd-linux-2010/",
    # "https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04",
    # "https://dev.mysql.com/doc/refman/5.7/en/copying-databases.html",
    # "https://blog.51cto.com/phpbk/108989",
    # "https://raspberrypi.stackexchange.com/questions/26836/possible-to-reinstall-x-server-and-use-graphical-after-having-removed-it",
    # "https://forums.raspberrypi.com/viewtopic.php?t=150438",
    # "https://www.htpcguides.com/configure-nfs-server-and-nfs-client-raspberry-pi/",
    # "https://blog.csdn.net/xdw1985829/article/details/38845533",
    # "https://wangye.org/blog/archives/845/",
    # "https://blog.mynook.info/post/boot-raspberrypi-from-external-hdd/",
    # "https://blog.gtwang.org/iot/raspberry-pi-vcgencmd-hardware-information/",
    # #"https://www.howtoforge.com/tutorial/how-to-connect-your-android-device-on-linux/",
    # "https://www.shuyz.com/posts/diy-stable-wifi-adapter-for-raspberry-pi/",
    # "https://www.htpcguides.com/install-readymedia-minidlna-1-1-4-raspberry-pi/",
    # "https://www.mivm.cn/openwrt-frp/",
    # "https://www.findhao.net/easycoding/1184",
    # "https://blog.csdn.net/guanmaoning/article/details/80283012",
    # "https://wenku.baidu.com/view/753bf819fad6195f312ba6d6.html",
    # "https://forums.raspberrypi.com/viewtopic.php?t=166098",
    # "https://mitchtech.net/vnc-setup-on-raspberry-pi-from-ubuntu/",
    # "https://googleprojectzero.blogspot.com/2018/01/reading-privileged-memory-with-side.html",
    # "https://raspberrypi.stackexchange.com/questions/40854/kernel-panic-not-syncing-vfs-unable-to-mount-root-fs-on-unknown-block179-6/40855",
    # "https://medium.com/@roniemeque/using-raspberry-pi-for-laravel-developing-30dabcdeba43"
    # ]
    # pages=[
    # "https://blog.csdn.net/machh/article/details/51299627",
    # "http://arondight.me/2016/02/17/%E4%BD%BF%E7%94%A8SSH%E5%8F%8D%E5%90%91%E9%9A%A7%E9%81%93%E8%BF%9B%E8%A1%8C%E5%86%85%E7%BD%91%E7%A9%BF%E9%80%8F/",
    # "https://www.polarxiong.com/archives/%E6%A0%91%E8%8E%93%E6%B4%BE%E5%88%A9%E7%94%A8nginx%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86-%E6%88%90%E4%B8%BAIPv6-IPv4%E5%85%AC%E7%BD%91%E6%9C%8D%E5%8A%A1%E5%99%A8-%E9%9C%80%E8%A6%81%E8%BF%9C%E7%A8%8B%E5%8F%8C%E6%A0%88%E6%9C%8D%E5%8A%A1%E5%99%A8.html",
    # "https://www.jianshu.com/p/3807dae958cf",
    # "https://www.zhukun.net/archives/8130",
    # "https://zhuanlan.zhihu.com/p/21471896",
    # "https://imququ.com/post/letsencrypt-certificate.html",
    # "https://www.iteye.com/blog/happysoul-2218060"
    # ]
    pages = [x for x in pages if x]
    pool = Pool(6)
    pool.map(runSpider, pages)
    pool.close()
    pool.join()

if __name__ == "__main__":
    try:
        os.mkdir("imgs")
    except FileExistsError:
        pass
    main()
    
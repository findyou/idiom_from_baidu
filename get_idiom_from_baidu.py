# -*- coding: utf-8 -*-
"""
@author: findyou
@contact: albert.peng@foxmail.com
@version: 1.0
@license: Apache Licence
@file: get_idiom_from_baidu.py
@time: 2018/10/21 20:35
"""

__author__ = 'albert'
__version__ = '1.0'

import json
import sqlite3

import os
import requests
import socket
import time
import sys

# 总页数，直接手动，不去获取了
page_count = 1546

url='https://hanyu.baidu.com/hanyu/ajax/search_list?wd=%E6%88%90%E8%AF%AD&from=poem&pn={}&_={}'

# 组装请求头
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}
# 默认数据库
db_filename = 'idiom.sqlite3'


def get_idiom_data(start_pagenum=1, end_pagenum=10,all=False):
    '''
      爬取百度成语数据，解析并保存到数据到数据库
      :param start_pagenum: 默认从第1页开始
      :param end_pagenum: 默认第10页结束
      '''
    global page_count, header,url

    # 统计成语条数
    idiom_count = 0
    # 进度条
    page_num = 0
    get_url=url.format(1, int(round(time.time() * 1000)))

    # 连接数据库
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # 获取全部成语
    if all: end_pagenum = page_count

    for i in range(start_pagenum, end_pagenum + 1):
        # 当前时间戳
        # t = int(round(time.time() * 1000))
        # 模拟请求获取json数据
        try:
            # 自动保存cookie
            s = requests.session()
            header['Referrer'] = get_url

            # 百度 ajax 成语请求API
            get_url = url.format(i, int(round(time.time() * 1000)))

            # 模拟请求
            result = s.get(get_url, headers=header)
            # 判断请求是否成功
            if result.status_code == 200:
                res = json.loads(result.text)
                page_count = res['extra']['total-page']
                # 得到返回的成语
                for a in range(len(res['ret_array'])):
                    txt = res['ret_array'][a]
                    # 条数递增
                    idiom_count += 1

                    # 目前只需：成语、拼音
                    name = (get_vaule(txt, 'name'))[0].strip()
                    pinyin = (get_vaule(txt, 'pinyin'))[0].strip()
                    pinyin_list = pinyin.split(" ")

                    # 例句
                    # liju = get_vaule(txt, 'liju')[0]
                    ### 出处
                    # tmp = get_vaule(txt, 'source')[0]
                    # if len(tmp) > 0:
                    #     source = tmp.replace('"', '').replace("'", "").replace('\n', '')
                    # else:
                    #     source = ''
                    ### 同义词
                    # get_vaule(txt, 'synonym')
                    # tmp = get_vaule(txt, 'term_synonym')
                    # if len(tmp) > 0:
                    #     synonym = tmp
                    # else:

                    # ID，成语，拼音，成语首字，尾字，首拼，尾拼
                    cursor.execute(
                        'insert into IDIOM (ID,NAME,PINYIN,NAMEF,NAMEL,PINYINF,PINYINL) values (NULL,"%s","%s","%s","%s","%s","%s")' %
                        (name, pinyin, name[0], name[len(name) - 1], pinyin_list[0], pinyin_list[len(pinyin_list) - 1]))
        except requests.exceptions.ConnectTimeout as e:
            print("http请求超时！" + str(e))
        except socket.timeout as e:
            print("请求超时！ " + str(e))
        except socket.error as e:
            print("请求错误！" + str(e))
        # 进度条
        page_num += 1
        view_bar(page_num, end_pagenum)
    print('\n本次爬取[百度成语] :  第 ' + str(start_pagenum) + ' 至 ' +
          str(end_pagenum) + ' 页，共计 ' + str(idiom_count) + ' 条')

    cursor.close()
    conn.commit()
    conn.close()

def view_bar(num, total):
    '''进度条'''
    rate = num / total
    rate_num = int(rate * 100)
    # r = '\r %d%%' %(rate_num)
    r = '\r[%s>] %d%%' % ('=' * rate_num, rate_num)
    sys.stdout.write(r)
    sys.stdout.flush


def get_vaule(idiom_dict, key_vaule):
    if key_vaule in idiom_dict.keys():
        return idiom_dict[key_vaule]
    else:
        return [' ']


def init_db(filename=db_filename):
    '''
     如果数据库不存在，自动在当前目录创建idiom.sqlite3:
    '''
    if not os.path.exists(filename):
        conn = sqlite3.connect(filename)
        # 创建一个Cursor:
        cursor = conn.cursor()
        # 建表ID 自增长key
        cursor.execute(
            'CREATE TABLE IDIOM (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME VARCHAR(100),NAMEF VARCHAR(10),NAMEL VARCHAR(10),\
              PINYIN VARCHAR(100),PINYINF VARCHAR(10),PINYINL VARCHAR(10))')
        # 关闭Cursor:
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()


if __name__ == '__main__':
    # 初始化数据库
    init_db()

    # 获取1-10页的数据，数据库只会往里一直加数据，未做去重，所以以下三个方式，用最后一种。
    # get_idiom_data()

    # 获取x-x页的数据
    # get_idiom_data(start_pagenum=10,end_pagenum=50)

    # 获取所有数据
    get_idiom_data(all=True)
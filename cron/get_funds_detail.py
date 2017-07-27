import base

import sys
import pandas as pd
import json
from collections import namedtuple
import re
import ngender
from bs4 import BeautifulSoup
import numpy as np
import urllib

# my private modules
import fund_scanner.database
import fund_scanner.readurl

url = 'http://fund.eastmoney.com/%s.html'

def read_funds_detail( funds_code='000001' ):
    print('reading ', funds_code)
    ret = {}
    html = fund_scanner.readurl.simple_read_from_url(url%funds_code)
    soup = BeautifulSoup(html, 'lxml')
    match = re.search('基金类型：(.*)', soup.select('div.infoOfFund td')[0].text)
    s = match.group(1)
    s = s.split('|')
    s = s[0].replace(u'\xa0', '')
    ret['funds_type'] = s
    ret['funds_start_date'] = soup.select('div.infoOfFund td')[3].text.replace('成 立 日：', '')
    ret['recent_1_month'] = soup.select('div.dataOfFund .dataItem01 dd')[1].select('span.ui-num')[0].text
    ret['recent_3_month'] = soup.select('div.dataOfFund .dataItem02 dd')[1].select('span.ui-num')[0].text
    ret['recent_6_month'] = soup.select('div.dataOfFund .dataItem03 dd')[1].select('span.ui-num')[0].text
    ret['recent_1_year']  = soup.select('div.dataOfFund .dataItem01 dd')[2].select('span.ui-num')[0].text
    ret['recent_3_year']  = soup.select('div.dataOfFund .dataItem02 dd')[2].select('span.ui-num')[0].text
    ret['recent_total']   = soup.select('div.dataOfFund .dataItem03 dd')[2].select('span.ui-num')[0].text
    ret['funds_price'] = soup.select('div.dataOfFund .dataItem02 dd')[0].select('span.ui-num')[0].text
    ret['funds_price_adjust'] = soup.select('div.dataOfFund .dataItem03 dd')[0].select('span.ui-num')[0].text
    match = re.search('基金规模：([\d\.]+)亿元', soup.select('div.infoOfFund td')[1].text)
    ret['funds_amount'] = match.group(1)
    return ret
    
# read_funds_detail('000775')

def extract_percentage(s, key):
    ret = None
    try:
        ret = float(s[key].strip('%'))
    finally:
        return ret


with fund_scanner.database.get_connection() as cursor:

    #Read records
    sql = 'select * from `funds` where 1 order by `update_time` limit 0,1;'
    cursor.execute(sql)
    result = cursor.fetchall()

    #fetch the detail data
    for item in result:
        dic = read_funds_detail(item['funds_code'])

        sql = 'update `funds` set `funds_type`=%s, `funds_start_date`=%s, `update_time`=Now() where `funds_code`=%s;'
        cursor.execute(sql, (dic['funds_type'], dic['funds_start_date'], item['funds_code']))

        columns_to_update = ['funds_price', 'funds_price_adjust', 'funds_amount',
                            'funds_recent_1_month', 'funds_recent_3_month', 'funds_recent_6_month',
                            'funds_recent_1_year', 'funds_recent_3_year', 'funds_return_total']

        sql = 'INSERT INTO `funds_update` ' +\
                '(`funds_id`, `'+('`, `'.join(columns_to_update))+'`, `update_time`) '+\
                'VALUES ('+'%s,'*10+' Now()) ON DUPLICATE KEY UPDATE '+\
                '`'+('`=%s, `'.join(columns_to_update))+'`=%s, `update_time`=Now();'

        funds_price = extract_percentage(dic,'funds_price')
        funds_price_adjust = extract_percentage(dic,'funds_price_adjust')
        funds_amount = extract_percentage(dic,'funds_amount')
        recent_1_month = extract_percentage(dic,'recent_1_month')
        recent_3_month = extract_percentage(dic,'recent_3_month')
        recent_6_month = extract_percentage(dic,'recent_6_month')
        recent_1_year = extract_percentage(dic,'recent_1_year')
        recent_3_year = extract_percentage(dic,'recent_3_year')
        recent_total = extract_percentage(dic,'recent_total')
        cursor.execute(sql, (int(item['funds_id']), 
                             funds_price, funds_price_adjust, funds_amount,
                             recent_1_month, recent_3_month, recent_6_month, recent_1_year, recent_3_year, recent_total, 
                             funds_price, funds_price_adjust, funds_amount,
                             recent_1_month, recent_3_month, recent_6_month, recent_1_year, recent_3_year, recent_total))


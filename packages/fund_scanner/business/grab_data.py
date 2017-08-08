from bs4 import BeautifulSoup
import re
import time

# my private modules
import fund_scanner.common_tools.database as db
import fund_scanner.common_tools.readurl
import fund_scanner.common_tools.others as others
import fund_scanner.common_tools.logger as logger

@logger.enter_exit_logger
def get_funds(funds_code):
    first_run = True
    ret = {}
    url = 'http://fund.eastmoney.com/%s.html'
    if type(funds_code)==str:
        funds_code = [funds_code]
    for each_code in funds_code:
        if first_run:
            first_run = False
        else:
            time.sleep(1)
        all_required_columns = ['funds_name_full', 'funds_type', 'funds_start_date', 'funds_amount',
        'funds_recent_1_month', 'funds_recent_3_month', 'funds_recent_6_month', 'funds_recent_1_year',
        'funds_recent_3_year', 'funds_return_total', 'funds_price', 'funds_price_adjust']
        each_ret = {w:None for w in all_required_columns}
        try:
            html = fund_scanner.common_tools.readurl.simple_read_from_url(url%each_code)
            soup = BeautifulSoup(html, 'lxml')

            title = soup.select('div.fundDetail-tit')[0]
            matches = re.search('(%s?)\('%others.re_utf_char(), title.text)
            if matches is not None:
                each_ret['funds_name_full'] = matches.group(1)

            for each_info in soup.select('div.infoOfFund td'):
                labels_meaning = [
                                    ['基金类型', 'funds_type', others.re_utf_char()],
                                    ['成 立 日', 'funds_start_date', others.re_utf_char()],
                                    ['基金规模', 'funds_amount', others.re_numbers()]
                                ]
                for each_label in labels_meaning:
                    matches = re.search('%s：(%s)'%(each_label[0], each_label[2]), each_info.text)
                    if matches is not None:
                        if each_label[2]==others.re_numbers():
                            each_ret[each_label[1]] = float(matches.group(1))
                        else:
                            each_ret[each_label[1]] = matches.group(1)

            for each_data in soup.select('div.dataOfFund dd'):
                labels_meaning = [
                                    ['近1月', 'funds_recent_1_month', others.re_numbers()],
                                    ['近3月', 'funds_recent_3_month', others.re_numbers()],
                                    ['近6月', 'funds_recent_6_month', others.re_numbers()],
                                    ['近1年', 'funds_recent_1_year', others.re_numbers()],
                                    ['近3年', 'funds_recent_3_year', others.re_numbers()],
                                    ['成立来', 'funds_return_total', others.re_numbers()]
                                ]
                for each_label in labels_meaning:
                    matches = re.search('%s：(%s)'%(each_label[0], each_label[2]), each_data.text)
                    if matches is not None:
                        if matches.group(1)[:2] != '--':
                            if each_label[2]==others.re_numbers():
                                each_ret[each_label[1]] = float(matches.group(1))
                            else:
                                each_ret[each_label[1]] = matches.group(1)

            for each_data in soup.select('div.dataOfFund dl'):
                labels_meaning = [
                                    ['单位净值 \(.*?\)', 'funds_price', others.re_numbers()],
                                    ['累计净值', 'funds_price_adjust', others.re_numbers()]
                                ]
                for each_label in labels_meaning:
                    matches = re.search('%s(%s)'%(each_label[0], each_label[2]), each_data.text)
                    if matches is not None:
                        if matches.group(1)[:2] != '--':
                            if each_label[2]==others.re_numbers():
                                each_ret[each_label[1]] = float(matches.group(1))
                            else:
                                each_ret[each_label[1]] = matches.group(1)

            ret[each_code] = each_ret
        except ConnectionResetError:
            logger.logger.warning('Connection Reset by Peer.')
        except:
            logger.logger.warning('Other error.')
    return ret

@logger.enter_exit_logger
def write_funds_to_database(funds):
    with db.get_connection() as cursor:
        for funds_code, each_fund in funds.items():
            sql = 'INSERT INTO funds (funds_code, funds_name_full, funds_type, funds_start_date, update_time)'\
            ' VALUES (%s,%s,%s,%s,Now()) ON DUPLICATE KEY '\
            'UPDATE funds_name_full=%s, funds_type=%s, funds_start_date=%s, update_time=Now();'
            cursor.execute(sql, (funds_code, each_fund['funds_name_full'], each_fund['funds_type'], each_fund['funds_start_date'], each_fund['funds_name_full'], each_fund['funds_type'], each_fund['funds_start_date']))
            funds_id = cursor.lastrowid

            columns_to_update = ['funds_price', 'funds_price_adjust', 'funds_amount',
                                'funds_recent_1_month', 'funds_recent_3_month', 'funds_recent_6_month',
                                'funds_recent_1_year', 'funds_recent_3_year', 'funds_return_total']

            sql = 'INSERT INTO `funds_update` (`funds_id`, `'+('`, `'.join(columns_to_update))+'`, `update_time`) '\
            ' VALUES ('+'%s,'*10+' Now()) ON DUPLICATE KEY '\
            'UPDATE `'+('`=%s, `'.join(columns_to_update))+'`=%s, `update_time`=Now();'
            cursor.execute(sql, 
                tuple([funds_id]+[each_fund[w] for w in columns_to_update]+[each_fund[w] for w in columns_to_update]))

@logger.enter_exit_logger
def update_funds(funds_code):
    write_funds_to_database(get_funds(funds_code))


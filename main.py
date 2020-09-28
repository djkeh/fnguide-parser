#!/user/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import requests
import csv
import logging
from time import sleep
from random import random
from bs4 import BeautifulSoup
from pprint import pprint


def wait():
    second = lambda : random() / 2 + 0.5
    sleep(second())

def get_html(gicode):
    url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp'
    param = {'gicode': gicode}
    r = requests.get(url, params = param)

    wait()

    return r.text

def parse(text, gicode):
    annual_number = 3
    net_quarter_number = 7
    max_table_column_length = 8

    soup = BeautifulSoup(text, "lxml")

    if not soup.find(id = 'highlight_D_A'):
        # 투자회사 종목은 금융감독원 전자공시시스템에 사업보고서를 공시하지 않아서 재무정보가 없다고 한다
        return None

    corp_name           = soup.find(id = 'giName').text # 기업명
    header_rows         = soup.find(id = 'highlight_D_A').thead.find_all('tr')
    header_titles       = header_rows[1].find_all('th')

    if len(header_titles) != max_table_column_length:
        # 일부 종목은 연간 보고자료가 나오지 않은 경우가 있다. 이 경우는 스킵
        return None

    annual_header       = header_titles[annual_number].span.text # Annual 헤더
    net_quarter_header  = header_titles[net_quarter_number].span.text # Net Quarter 헤더


    body_rows           = soup.find(id = 'highlight_D_A').tbody.find_all('tr')
    revenue_title       = body_rows[0].th.text # 매출액 타이틀
    profit_title        = body_rows[1].th.text # 영업이익 타이틀
    profit2_title       = body_rows[2].th.text # 영업이익(발표기준) 타이틀
    row3_title          = body_rows[3].th.text # 당기순이익 타이틀
    row4_title          = body_rows[4].th.text # 지배주주순이익 타이틀
    row5_title          = body_rows[5].th.text # 비지배주주순이익 타이틀
    row6_title          = body_rows[6].th.text # 자산총계 타이틀
    row7_title          = body_rows[7].th.text # 부채총계 타이틀
    row8_title          = body_rows[8].th.text # 자본총계 타이틀
    row9_title          = body_rows[9].th.text # 지배주주지분 타이틀
    row10_title         = body_rows[10].th.text # 비지배주주지분 타이틀
    roe_title           = body_rows[17].th.span.text # roe 타이틀

    annual_revenue      = body_rows[0].find_all('td')[annual_number].text # 연간 매출액 값
    annual_profit       = body_rows[1].find_all('td')[annual_number].text # 연간 영업이익 값
    annual_profit2      = body_rows[2].find_all('td')[annual_number].text # 연간 영업이익(발표기준) 값
    annual_3            = body_rows[3].find_all('td')[annual_number].text # 연간 당기순이익 값
    annual_4            = body_rows[4].find_all('td')[annual_number].text # 연간 지배주주순이익 값
    annual_5            = body_rows[5].find_all('td')[annual_number].text # 연간 비지배주주순이익 값
    annual_6            = body_rows[6].find_all('td')[annual_number].text # 연간 자산총계 값
    annual_7            = body_rows[7].find_all('td')[annual_number].text # 연간 부채총계 값
    annual_8            = body_rows[8].find_all('td')[annual_number].text # 연간 자본총계 값
    annual_9            = body_rows[9].find_all('td')[annual_number].text # 연간 지배주주지분 값
    annual_10           = body_rows[10].find_all('td')[annual_number].text # 연간 비지배주주지분 값
    annual_roe          = body_rows[17].find_all('td')[annual_number].text # 연간 roe 값

    net_quarter_revenue = body_rows[0].find_all('td')[net_quarter_number].text # 분기 매출액 값
    net_quarter_profit  = body_rows[1].find_all('td')[net_quarter_number].text # 분기 영업이익 값
    net_quarter_profit2 = body_rows[2].find_all('td')[net_quarter_number].text # 분기 영업이익(발표기준) 값
    net_quarter_3       = body_rows[3].find_all('td')[net_quarter_number].text # 분기 당기순이익 값
    net_quarter_4       = body_rows[4].find_all('td')[net_quarter_number].text # 분기 지배주주순이익 값
    net_quarter_5       = body_rows[5].find_all('td')[net_quarter_number].text # 분기 비지배주주순이익 값
    net_quarter_6       = body_rows[6].find_all('td')[net_quarter_number].text # 분기 자산총계 값
    net_quarter_7       = body_rows[7].find_all('td')[net_quarter_number].text # 분기 부채총계 값
    net_quarter_8       = body_rows[8].find_all('td')[net_quarter_number].text # 분기 자본총계 값
    net_quarter_9       = body_rows[9].find_all('td')[net_quarter_number].text # 분기 지배주주지분 값
    net_quarter_10      = body_rows[10].find_all('td')[net_quarter_number].text # 분기 비지배주주지분 값
    net_quarter_roe     = body_rows[17].find_all('td')[net_quarter_number].text # 분기 roe 값


    result                      = {}
    result['corp_name']         = {'title': '회사명',                                   'value': corp_name}
    result['gicode']            = {'title': '종목코드',                                 'value': gicode}
    result['annual_revenue']    = {'title': revenue_title + ' ' + annual_header,        'value': format(annual_revenue)}
    result['annual_profit']     = {'title': profit_title + ' ' + annual_header,         'value': format(annual_profit)}
    result['annual_profit2']    = {'title': profit2_title + ' ' + annual_header,        'value': format(annual_profit2)}
    result['annual_3']          = {'title': row3_title + ' ' + annual_header,           'value': format(annual_3)}
    result['annual_4']          = {'title': row4_title + ' ' + annual_header,           'value': format(annual_4)}
    result['annual_5']          = {'title': row5_title + ' ' + annual_header,           'value': format(annual_5)}
    result['annual_6']          = {'title': row6_title + ' ' + annual_header,           'value': format(annual_6)}
    result['annual_7']          = {'title': row7_title + ' ' + annual_header,           'value': format(annual_7)}
    result['annual_8']          = {'title': row8_title + ' ' + annual_header,           'value': format(annual_8)}
    result['annual_9']          = {'title': row9_title + ' ' + annual_header,           'value': format(annual_9)}
    result['annual_10']         = {'title': row10_title + ' ' + annual_header,          'value': format(annual_10)}
    result['annual_roe']        = {'title': roe_title + ' ' + annual_header,            'value': format(annual_roe)}
    result['quarter_revenue']   = {'title': revenue_title + ' ' + net_quarter_header,   'value': format(net_quarter_revenue)}
    result['quarter_profit']    = {'title': profit_title + ' ' + net_quarter_header,    'value': format(net_quarter_profit)}
    result['quarter_profit2']   = {'title': profit2_title + ' ' + net_quarter_header,   'value': format(net_quarter_profit2)}
    result['quarter_3']         = {'title': row3_title + ' ' + net_quarter_header,      'value': format(net_quarter_3)}
    result['quarter_4']         = {'title': row4_title + ' ' + net_quarter_header,      'value': format(net_quarter_4)}
    result['quarter_5']         = {'title': row5_title + ' ' + net_quarter_header,      'value': format(net_quarter_5)}
    result['quarter_6']         = {'title': row6_title + ' ' + net_quarter_header,      'value': format(net_quarter_6)}
    result['quarter_7']         = {'title': row7_title + ' ' + net_quarter_header,      'value': format(net_quarter_7)}
    result['quarter_8']         = {'title': row8_title + ' ' + net_quarter_header,      'value': format(net_quarter_8)}
    result['quarter_9']         = {'title': row9_title + ' ' + net_quarter_header,      'value': format(net_quarter_9)}
    result['quarter_10']        = {'title': row10_title + ' ' + net_quarter_header,     'value': format(net_quarter_10)}
    result['quarter_roe']       = {'title': roe_title + ' ' + net_quarter_header,       'value': format(net_quarter_roe)}

    return result

def format(str):
    return str.strip().replace(',', '')

def init_csv(data):
    with open('data.csv', 'w', newline = '', encoding = 'utf8') as csvfile:
        fieldnames = [ \
            data['corp_name']['title'], \
            data['gicode']['title'], \
            data['annual_revenue']['title'], \
            data['annual_profit']['title'], \
            data['annual_profit2']['title'], \
            data['annual_3']['title'], \
            data['annual_4']['title'], \
            data['annual_5']['title'], \
            data['annual_6']['title'], \
            data['annual_7']['title'], \
            data['annual_8']['title'], \
            data['annual_9']['title'], \
            data['annual_10']['title'], \
            data['annual_roe']['title'], \
            data['quarter_revenue']['title'], \
            data['quarter_profit']['title'], \
            data['quarter_profit2']['title'], \
            data['quarter_3']['title'], \
            data['quarter_4']['title'], \
            data['quarter_5']['title'], \
            data['quarter_6']['title'], \
            data['quarter_7']['title'], \
            data['quarter_8']['title'], \
            data['quarter_9']['title'], \
            data['quarter_10']['title'], \
            data['quarter_roe']['title'] \
            ]

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()

def export_to_csv(data):
    logging.debug("exporting: " + data['gicode']['value'])

    with open('data.csv', 'a', newline = '', encoding = 'utf8') as csvfile:
        fieldnames = [ \
            data['corp_name']['title'], \
            data['gicode']['title'], \
            data['annual_revenue']['title'], \
            data['annual_profit']['title'], \
            data['annual_profit2']['title'], \
            data['annual_3']['title'], \
            data['annual_4']['title'], \
            data['annual_5']['title'], \
            data['annual_6']['title'], \
            data['annual_7']['title'], \
            data['annual_8']['title'], \
            data['annual_9']['title'], \
            data['annual_10']['title'], \
            data['annual_roe']['title'], \
            data['quarter_revenue']['title'], \
            data['quarter_profit']['title'], \
            data['quarter_profit2']['title'], \
            data['quarter_3']['title'], \
            data['quarter_4']['title'], \
            data['quarter_5']['title'], \
            data['quarter_6']['title'], \
            data['quarter_7']['title'], \
            data['quarter_8']['title'], \
            data['quarter_9']['title'], \
            data['quarter_10']['title'], \
            data['quarter_roe']['title'] \
            ]

        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writerow({ \
            data['corp_name']['title']: data['corp_name']['value'], \
            data['gicode']['title']: data['gicode']['value'], \
            data['annual_revenue']['title']: data['annual_revenue']['value'], \
            data['annual_profit']['title']: data['annual_profit']['value'], \
            data['annual_profit2']['title']: data['annual_profit2']['value'], \
            data['annual_3']['title']: data['annual_3']['value'], \
            data['annual_4']['title']: data['annual_4']['value'], \
            data['annual_5']['title']: data['annual_5']['value'], \
            data['annual_6']['title']: data['annual_6']['value'], \
            data['annual_7']['title']: data['annual_7']['value'], \
            data['annual_8']['title']: data['annual_8']['value'], \
            data['annual_9']['title']: data['annual_9']['value'], \
            data['annual_10']['title']: data['annual_10']['value'], \
            data['annual_roe']['title']: data['annual_roe']['value'], \
            data['quarter_revenue']['title']: data['quarter_revenue']['value'], \
            data['quarter_profit']['title']: data['quarter_profit']['value'], \
            data['quarter_profit2']['title']: data['quarter_profit2']['value'], \
            data['quarter_3']['title']: data['quarter_3']['value'], \
            data['quarter_4']['title']: data['quarter_4']['value'], \
            data['quarter_5']['title']: data['quarter_5']['value'], \
            data['quarter_6']['title']: data['quarter_6']['value'], \
            data['quarter_7']['title']: data['quarter_7']['value'], \
            data['quarter_8']['title']: data['quarter_8']['value'], \
            data['quarter_9']['title']: data['quarter_9']['value'], \
            data['quarter_10']['title']: data['quarter_10']['value'], \
            data['quarter_roe']['title']: data['quarter_roe']['value'] \
            })

def read_codes():
    gicodes = []

    with open('gicodes.txt', 'r', encoding = 'utf8') as file:
        for row in file:
            gicodes.append(row.rstrip())

    return gicodes


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: main [gicode]')
        sys.exit(1)

    gicodes = args[0].split(',')
    html = get_html(gicodes[0])
    data = parse(html, gicodes[0])

    init_csv(data)

    for gicode in read_codes():
        html = get_html(gicode)
        data = parse(html, gicode)

        if data:
            export_to_csv(data)


if __name__ == '__main__':
    main()
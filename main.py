#!/user/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import requests
import csv
from bs4 import BeautifulSoup
from pprint import pprint


def get_html(gicode):
    url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp'
    param = {'gicode': gicode}
    r = requests.get(url, params = param)

    return r.text

def parse(text, gicode):
    annual_number = 3
    net_quarter_number = 7

    soup = BeautifulSoup(text, "lxml")

    corp_name           = soup.find(id = 'giName').text # 기업명

    header_rows         = soup.find(id = 'highlight_D_A').thead.find_all('tr')
    annual_header       = header_rows[1].find_all('th')[annual_number].span.text # Annual 헤더
    net_quarter_header  = header_rows[1].find_all('th')[net_quarter_number].span.text # Net Quarter 헤더

    body_rows           = soup.find(id = 'highlight_D_A').tbody.find_all('tr')
    revenue_title       = body_rows[0].th.text # 매출액 타이틀
    profit_title        = body_rows[1].th.text # 영업이익 타이틀
    roe_title           = body_rows[17].th.span.text # roe 타이틀
    annual_revenue      = body_rows[0].find_all('td')[annual_number].text # 연간 매출액 값
    annual_profit       = body_rows[1].find_all('td')[annual_number].text # 연간 매출액 값
    annual_roe          = body_rows[17].find_all('td')[annual_number].text # 연간 매출액 값
    net_quarter_revenue = body_rows[0].find_all('td')[net_quarter_number].text # 연간 매출액 값
    net_quarter_profit  = body_rows[1].find_all('td')[net_quarter_number].text # 연간 매출액 값
    net_quarter_roe     = body_rows[17].find_all('td')[net_quarter_number].text # 연간 매출액 값

    result                      = {}
    result['corp_name']         = {'title': '회사명',                                   'value': corp_name}
    result['gicode']            = {'title': '종목코드',                                 'value': gicode}
    result['annual_revenue']    = {'title': revenue_title + ' ' + annual_header,        'value': format(annual_revenue)}
    result['annual_profit']     = {'title': profit_title + ' ' + annual_header,         'value': format(annual_profit)}
    result['annual_roe']        = {'title': roe_title + ' ' + annual_header,            'value': format(annual_roe)}
    result['quarter_revenue']   = {'title': revenue_title + ' ' + net_quarter_header,   'value': format(net_quarter_revenue)}
    result['quarter_profit']    = {'title': profit_title + ' ' + net_quarter_header,    'value': format(net_quarter_profit)}
    result['quarter_roe']       = {'title': roe_title + ' ' + net_quarter_header,       'value': format(net_quarter_roe)}

    return result

def format(str):
    return str.replace('\xa0', '')

def export_to_csv(data):
    with open('data.csv', 'w', newline = '') as csvfile:
        fieldnames = [ \
            data['corp_name']['title'], \
            data['gicode']['title'], \
            data['annual_revenue']['title'], \
            data['annual_profit']['title'], \
            data['annual_roe']['title'], \
            data['quarter_revenue']['title'], \
            data['quarter_profit']['title'], \
            data['quarter_roe']['title'] \
            ]
        
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()
        writer.writerow({ \
            data['corp_name']['title']: data['corp_name']['value'], \
            data['gicode']['title']: data['gicode']['value'], \
            data['annual_revenue']['title']: data['annual_revenue']['value'], \
            data['annual_profit']['title']: data['annual_profit']['value'], \
            data['annual_roe']['title']: data['annual_roe']['value'], \
            data['quarter_revenue']['title']: data['quarter_revenue']['value'], \
            data['quarter_profit']['title']: data['quarter_profit']['value'], \
            data['quarter_roe']['title']: data['quarter_roe']['value'] \
            })


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: main [gicode]')
        sys.exit(1)

    gicode = args[0]
    html = get_html(gicode)
    data = parse(html, gicode)

    pprint(data)
    export_to_csv(data)

# Main body
if __name__ == '__main__':
    main()
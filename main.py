#!/user/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def getHtml(gicode):
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

    result              = {}
    result['corp_name'] = {'title': '회사명',       'data': corp_name}
    result['gicode']    = {'title': '종목코드',     'data': gicode}
    result['revenue']   = {'title': revenue_title,  'data': {annual_header: format(annual_revenue), net_quarter_header: format(net_quarter_revenue)}}
    result['profit']    = {'title': profit_title,   'data': {annual_header: format(annual_profit),  net_quarter_header: format(net_quarter_profit)}}
    result['roe']       = {'title': roe_title,      'data': {annual_header: format(annual_roe),     net_quarter_header: format(net_quarter_roe)}}

    return result

def format(str):
    return str.replace('\xa0', '')

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: main [gicode]')
        sys.exit(1)

    gicode = args[0]
    html = getHtml(gicode)
    data = parse(html, gicode)

    pprint(data)

# Main body
if __name__ == '__main__':
    main()
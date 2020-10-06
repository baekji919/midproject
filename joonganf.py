from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import pandas as pd
import requests
from lxml.html import fromstring
from openpyxl import Workbook
import time

def main(page_num, keyword, start_date, end_date, type, match_keyword, include_keyword, file_name):
    TARGET_URL_BEFORE_KEYWORD = '&Keyword='
    TARGET_URL_BEFORE_START_DATE = '&PeriodType=DirectInput&StartSearchDate='
    TARGET_URL_BEFORE_END_DATE = '&EndSearchDate='
    TARGET_URL_BEFORE_TYPE = '&SortType=New&SourceGroupType=Joongang&ServiceCode='
    TARGET_URL_BEFORE_MATCH_KEYWORD = '&SearchCategoryType=TotalNews&MatchKeyword='
    TARGET_URL_BEFORE_INCLUDE_KEYWORD = '&IncludeKeyword='

    if type == '뉴스':
        type = '10'
    elif type == '사설':
        type = '20'
    else:
        print('다시 입력하세요')

    # links = []
    dates = []
    texts = []
    titles = []
    for i in range(1, page_num + 1):
        TARGET_URL_BEFORE_PAGE_NUM = "https://news.joins.com/Search/TotalNews?page={}".format(i)
        url = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEYWORD \
              + quote(keyword) + TARGET_URL_BEFORE_START_DATE \
              + quote(start_date) + TARGET_URL_BEFORE_END_DATE \
              + quote(end_date) + TARGET_URL_BEFORE_TYPE\
              + quote(type) + TARGET_URL_BEFORE_MATCH_KEYWORD \
              + quote(match_keyword) + TARGET_URL_BEFORE_INCLUDE_KEYWORD + quote(include_keyword)
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, 'html.parser')

        for href in soup.find('div', class_='section_news').find_all('li'):
            # link = href.find('a')['href']
            # links.append(link)

            date = href.find('span', 'byline').find_all('em')[1].string
            dates.append(date)

            title = href.find('h2', 'headline mg').get_text()
            titles.append(title)

            res = requests.get(link)
            parser = fromstring(res.text)
            article_form = parser.xpath('//*[@id="body"]')[0]
            article_body = article_form.xpath('.//div[@id="article_body"]')[0].text_content()
            if article_body == "":
                # Nan값 일경우 임의 데이터 삽입
                texts.append("aaa")
            else:
                texts.append(article_body.strip().split())


    df = pd.DataFrame({"date":dates,"title":titles,"text":texts})
    df.to_excel('C:/PycharmProject/crawl/'+ quote(file_name), index = False)
    # excel_writer = pd.ExcelWriter('C:/Users/Baek JiHyun/PycharmProjects/testt/crawl/covid_news.xlsx', engine = 'xlsxwriter')
    # df.to_excel(excel_writer, index = False)
    time.sleep(5)

main(7, '메르스', '2015.05.20', '2015.08.20', '뉴스', '정부', '대응', 'mers_news.xlsx')
main(10, '메르스', '2015.05.20', '2015.08.20', '사설', '정부', '대응', 'mers_opinion.xlsx')
main(53, '코로나', '2020.01.20', '2020.04.20', '뉴스', '정부', '대응', 'covid_news.xlsx')
main(22, '코로나', '2020.01.20', '2020.04.20', '사설', '정부', '대응', 'covid_opinion.xlsx')

# main(1, '메르스', '2015.05.20', '2015.08.20', '뉴스', '정부', '대응', 'mers_t1.xlsx')
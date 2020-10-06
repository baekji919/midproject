from konlpy.tag import Kkma
import pandas as pd
import numpy as np
from openpyxl import load_workbook

kkma = Kkma()

print(kkma.morphs(u'심상정 정의당 대표가 20일 서울 여의도 국회에서 열린 상무위원회의에서 모두발언을 하고 있다'))


#data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
load_wb = load_workbook("C:/PycharmProject/crawl/covid_news.xlsx", data_only=True)
#시트 이름으로 불러오기
load_ws = load_wb['Sheet1']

#셀 주소로 값 출력
df = load_ws['C2'].value
print(df)

print('\n-----지정한 셀 출력-----')
get_cells = load_ws['C2':'C10']
for row in get_cells:
        for cell in row:
            print(cell.value, '\n')

df = pd.read_csv("testProject/data/polarity.csv", encoding="cp949")

df1 = df.query("value in ['POS','NEG','NEUT']").reset_index().drop("index", axis=1)[['ngram', 'value']]

list = []
for i in df1['value']:
    if i == "POS":
        list.append(1)
    elif i == "NEG":
        list.append(-1)
    else:
        list.append(0)

df1['value'] = list

# df1.to_csv("testProject/data/file.csv",encoding="cp949")
df1.to_csv("testProject/data/file.csv", encoding="cp949", index=False)




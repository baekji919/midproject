# 2020/06/18(목) 최신 본
from konlpy.tag import Kkma
import pandas as pd
import numpy as np

kkma = Kkma()
# 형태소 CSV 파일 불러오기 : polarity.csv
polarity_df = pd.read_csv("C:/mid_project/lexicon/polarity.csv", encoding="cp949")
# polarity에서 ngram, value 열만 가져오기
polarity_df = polarity_df.iloc[:, [0, 7]].query("value in ['POS', 'NEG', 'NEUT']").reset_index().drop(columns=["index"])

# stopwords.txt 파일 불러오기
stopwords_df = pd.read_csv("C:/mid_project/stopwords.txt", encoding="utf-8", header=0)
# stopwords 데이터프레임 리스트로 변환
stopwords_list = list(stopwords_df["head"])

# polarity_df의 value 열의 값 변경 (POS : 1, NEG : -1, NEUT : 0)
polarity_df.loc[polarity_df["value"] == "POS", "value"] = 1
polarity_df.loc[polarity_df["value"] == "NEG", "value"] = -1
polarity_df.loc[polarity_df["value"] == "NEUT", "value"] = 0

# 단일 형태소 데이터
polarity_semi_df = polarity_df.query('ngram.str.contains(";")', engine="python").reset_index().drop(columns=["index"])
# 다중 형태소 데이터
polarity_not_semi_df = polarity_df.query('not ngram.str.contains(";")', engine="python").reset_index().drop(
    columns=["index"])

sheet_names_list = ["사설", "정치"]

polarity_top = pd.DataFrame(columns=["pos", "pos_value", "neg", "neg_value"])
excel_writer = pd.ExcelWriter('C:/mid_project/finaldata/cor_20.xlsx', engine='xlsxwriter')

for sheet_name_value in sheet_names_list:

    # 뉴스 가져오기
    donga_pol_df = pd.read_excel("C:/mid_project/finaldata/jojoongdong_cor.xlsx",
                                 sheet_name=sheet_name_value).dropna().reset_index().drop(columns=["index"])
    # POS, NEG, NEUT, TOTAL 데이터 갯수를 저장할 변수
    emotion_list = []

    for index_one, news_text in enumerate(donga_pol_df['text']):

        add_text_str = str()
        for i in kkma.pos(news_text):
            add_text_str += "/".join(i) + ";"

        ngram_list = []

        for index, text in enumerate(polarity_semi_df['ngram']):
            # 뉴스 내용이 있을 경우에만 작업 수행
            if add_text_str.count(text) != 0:
                ngram_list.extend([list(polarity_semi_df.iloc[index]) for i in range(add_text_str.count(text))])
                add_text_str = add_text_str.replace(text, "", add_text_str.count(text))

        # 다중 형태소와 일치하는 데이터
        semi_df = pd.DataFrame(ngram_list, columns=["ngram", "value"])
        # 단일 형태소 데이터
        not_semi_df = pd.DataFrame(np.array(add_text_str.split(";"))[:, np.newaxis], columns=["ngram"]).query(
            "ngram != ''")
        # 단일 형태소와 일치하는 데이터
        merge_df = pd.merge(polarity_df, not_semi_df, on="ngram").query("ngram not in @stopwords_list")

        # 단일, 다중 형태소데이터 병합
        final_df = pd.concat([semi_df, merge_df])

        polarity_top = polarity_top.append(final_df, ignore_index=True)
        # POS, NEG, NEUT, TOTAL 데이터 갯수를 카운트 후 리스트에 삽입
        emotion_list.append([final_df[final_df["value"] == 1]["value"].count(),
                             final_df[final_df["value"] == -1]["value"].count(),
                             final_df[final_df["value"] == 0]["value"].count(),
                             final_df["value"].count()])

    # 데이터프레임에 POS, NEG, NEUT, TOTAL 열추가
    donga_pol_df[["pos", "neg", "neut", "total"]] = pd.DataFrame(np.array(emotion_list)[:, 0:4],
                                                                 columns=["pos", "neg", "neut", "total"])
    donga_pol_df.to_excel(excel_writer, index=False, sheet_name=sheet_name_value)

    # NNG(명사) 중 ;을 포함하지 않는 긍정/부정 단어 top5  데이터 프레임 생성
    neg_top5_keyword_seri = \
    polarity_top[polarity_top["value"] == -1].query('ngram.str.contains("NNG") and not ngram.str.contains(";")',
                                                    engine="python")["ngram"].value_counts().head(20)
    neg_top5_keyword_arr = np.c_[
        np.array([i[:-4] for i in neg_top5_keyword_seri.index]), np.array(neg_top5_keyword_seri.values)]

    pos_top5_keyword_seri = \
    polarity_top[polarity_top["value"] == 1].query('ngram.str.contains("NNG") and not ngram.str.contains(";")',
                                                   engine="python")["ngram"].value_counts().head(20)
    pos_top5_keyword_arr = np.c_[
        np.array([i[:-4] for i in pos_top5_keyword_seri.index]), np.array(pos_top5_keyword_seri.values)]

    pd.DataFrame(np.c_[pos_top5_keyword_arr, neg_top5_keyword_arr],
                 columns=["pos", "pos_value", "neg", "neg_value"]).to_excel(excel_writer, index=False,
                                                                            sheet_name=sheet_name_value + "pos&neg")

excel_writer.save()
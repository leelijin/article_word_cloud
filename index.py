import string
from urllib import request
from bs4 import BeautifulSoup
import jieba
import pandas
import numpy
import unicodedata
import sys

url = 'http://www.huaxi100.com/c/b612g02d64d'

resp = request.urlopen(url)
html_data = resp.read().decode('utf-8')

soup = BeautifulSoup(html_data, 'html.parser')

html_string = soup.find('section').get_text()

no_html_string = html_string.replace('\r', '').replace('\n', '')


tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))

def remove_punctuation(text):
    return text.translate(tbl)


clean_string = remove_punctuation(no_html_string)

cut_list = jieba.lcut(clean_string)

# print(", ".join(cut_list))

new_cut_list = [ x for x in cut_list if x.strip() != '' ]
print(new_cut_list)
exit()
words_df = pandas.DataFrame({'segment': new_cut_list})

stopwords = pandas.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='utf-8')
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

result_list = words_df.head()

# print(result_list)
# exit()
words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count": numpy.size})
words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)

stat_list = words_stat.head(20)

print(stat_list)

exit();

import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib

matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud  # 词云包

wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)  # 指定字体类型、字体大小和字体颜色
word_frequence = {x[0]: x[1] for x in words_stat.head(10).values}
# print(word_frequence)
word_frequence_list = []
for key in word_frequence:
    temp = (key, word_frequence[key])
    word_frequence_list.append(temp)

wordcloud = wordcloud.fit_words(dict(word_frequence_list))
plt.imshow(wordcloud)

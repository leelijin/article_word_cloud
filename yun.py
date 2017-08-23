import hashlib
import random
import string
import unicodedata
from urllib import request
from bs4 import BeautifulSoup
import sys
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

url = 'http://www.huaxi100.com/c/b612g02d64d'

resp = request.urlopen(url)
html_data = resp.read().decode('utf-8')

soup = BeautifulSoup(html_data, 'html.parser')

html_string = soup.find().get_text()

no_html_string = html_string.replace('\r', '').replace('\n', '')

#去除标点符号
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))


def remove_punctuation(text):
    return text.translate(tbl)


clean_string = remove_punctuation(no_html_string)

cut_text = " ".join(jieba.cut(clean_string))

jieba.set_dictionary("dict/dict.txt")
# TODO::增加更多自定义词典
jieba.load_userdict('dict/words.txt')

jieba.analyse.set_stop_words('dict/stopwords.txt')

jieba_cut_text = jieba.analyse.textrank(clean_string, topK=3000, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))

cut_list = [x for x in jieba_cut_text if x.strip() != '']

cut_text = " ".join(cut_list)

# Read the whole text.
text = cut_text

# print(text)
#
# exit();

# Generate a word cloud image
wordcloud = WordCloud(font_path="dict/simhei.ttf", background_color="white", max_font_size=80).generate(text)
# Display the generated image:
# the matplotlib way:

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
filename = ''.join([random.choice(string.ascii_letters+string.digits) for i in range(10)])
plt.savefig('img/wordcloud_%s.png' % filename)
plt.show()

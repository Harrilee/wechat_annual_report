"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/9/2022 10:32 PM
"""
import jieba

with open('./utils/stopwords.txt', encoding='utf-8') as f:
    stopwords = list(set(f.readlines()))
for i in range(len(stopwords)):
    stopwords[i] = stopwords[i][:-1]
stopwords += [' ', '\n', '\t', '\r\n']

def count(word_string, username=""):
    """
    :param word_string: 待分割字符
    :param username: 用户名，防止用户名称被判断为高频词
    :return:
    """
    cut_result = jieba.cut_for_search(word_string)
    word_count = dict()
    for r in cut_result:
        if r in word_count:
            word_count[r] += 1
        else:
            word_count[r] = 1
    keys = list(word_count.keys())
    for key in keys:
        if key.lower() in stopwords or key in username:
            word_count.pop(key)
    return sorted(word_count.items(), key=lambda d: d[1], reverse=True)


if __name__ == '__main__':
    word_string_list = open('test.txt', mode='r', encoding='utf8').readlines()
    new_word_string_list = list()
    for w in word_string_list:
        if w == '\n':
            continue
        w = w.replace('\n', '')
        new_word_string_list.append(w)
    word_string = ''.join(new_word_string_list)
    print(count(word_string))

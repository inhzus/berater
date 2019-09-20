# -*- coding: utf-8 -*-

import os

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

DATA_PREFIX = 'data/stu_man/'
DATA_FIRST_DIR = DATA_PREFIX + '00/'
DATA_SECOND_DIR = DATA_PREFIX + '02/'


class TermFreqInvDocFreq:
    return_dict = {}

    @staticmethod
    def parse_file():
        data = []
        root_path = os.listdir(DATA_FIRST_DIR)
        root_path.sort(key=lambda x: int(x[:-4]))
        for filename in root_path:
            with open(DATA_FIRST_DIR + filename, mode='r', encoding="utf-8") as f:
                for line in f.readlines():
                    data.append(line)
        return data

    @staticmethod
    def list_to_dict(word):
        bag_word = dict()
        for t in range(len(word)):
            bag_word[word[t]] = t
        return bag_word

    @staticmethod
    def out_result(bag_word, weight, input_word):
        number = []
        result = dict()
        for j in range(len(input_word)):
            if input_word[j] in bag_word:
                number.append(bag_word[input_word[j]])
        for k in range(len(number)):
            for i in range(len(weight)):
                if k == 0:
                    result[i] = weight[i][number[k]]
                else:
                    t = result[i]
                    result[i] = t + weight[i][number[k]]
        res = zip(result.values(), result.keys())
        result = sorted(res)
        return result

    def paragraph_choose(self, potential_article):
        data = []
        for i in range(len(potential_article)):
            with open(DATA_SECOND_DIR + str(potential_article[i]) + ".txt", "r",
                      encoding="utf-8") as f:
                for line in f:
                    self.return_dict[line] = potential_article[i]
                    data.append(line)
        return data

    def ttf_idf(self, input_word):
        # corpus = ["我 来到 北京 清华大学 清华大学 清华大学 清华大学 清华大学 清华大学 清华大学 清华大学 清华大学 清华大学 北京 北京 北京 北京 北京 北京 北京 北京 北京 北京 北京 北京",
        # 第一类文本切词后的结果，词之间以空格隔开 "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果 "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果 "我 爱 北京 天安门"]  #
        # 第四类文本的切词结果
        data = self.parse_file()
        vector_maker = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer = TfidfTransformer(smooth_idf=False)  # 该类会统计每个词语的tf-idf权值
        tf_idf = transformer.fit_transform(
            vector_maker.fit_transform(data))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        word = vector_maker.get_feature_names()  # 获取词袋模型中的所有词语
        bag_word = self.list_to_dict(word)
        weight = tf_idf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        # for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        #     print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        # for j in range(len(word)):
        #     print(word[j], weight[18][j])
        result_article = self.out_result(bag_word, weight, input_word)
        # print(result_article)
        rr = result_article[::-1]
        potential_article = []
        for i in range(5):
            potential_article.append(rr[i][1])
        data = self.paragraph_choose(potential_article)
        return data

    @staticmethod
    def lcs(ss1, ss2):
        s1 = ss1
        s2 = ss2
        total = 100000
        res = -1
        res_ = -1
        ans = [0, 0]
        while (res_ < 0 or res_ >= res) and res_ != 0:
            res = res_
            if res <= 0:
                ans = [0, 0]
            else:
                ans = [(res / total), (res / len(ss2))]
            big = -1
            small = 1000000
            size1 = len(s1) + 1
            size2 = len(s2) + 1
            # 程序多加一行，一列，方便后面代码编写
            chess = [[["", 0] for _ in list(range(size2))] for _ in list(range(size1))]
            for i in list(range(1, size1)):
                chess[i][0][0] = s1[i - 1]
            for j in list(range(1, size2)):
                chess[0][j][0] = s2[j - 1]
            # print("初始化数据：")
            # print(chess)
            for i in list(range(1, size1)):
                for j in list(range(1, size2)):
                    if s1[i - 1] == s2[j - 1]:
                        chess[i][j] = ['↖', chess[i - 1][j - 1][1] + 1]
                    elif chess[i][j - 1][1] > chess[i - 1][j][1]:
                        chess[i][j] = ['←', chess[i][j - 1][1]]
                    else:
                        chess[i][j] = ['↑', chess[i - 1][j][1]]
            # print("计算结果：")
            # print(chess)
            i = size1 - 1
            j = size2 - 1
            s3 = []
            while i > 0 and j > 0:
                if chess[i][j][0] == '↖':
                    s3.append(chess[i][0][0])
                    big = max(big, i)
                    small = min(small, i)
                    # print(i)
                    i -= 1
                    j -= 1
                if chess[i][j][0] == '←':
                    j -= 1
                if chess[i][j][0] == '↑':
                    i -= 1
            s3.reverse()
            total = min(total, big - small + 1)
            res_ = len(s3)
            if big >= 0:
                s1 = s1[:big - 1] + s1[big:]
            # print("最长公共子序列：%s" % ''.join(s3))
        return ans

    @staticmethod
    def cut(x):
        return ' '.join([a for a in jieba.cut(x)])

    @staticmethod
    def cut2(x):
        data = []
        for i in jieba.cut(x):
            data.append(i)
        return data

    @staticmethod
    def f(doc, que):
        common = set([x for x in que if x in doc])
        total = len(common)
        if total == 0:
            return [0, 0]
        for i in range(total, len(doc)):
            for j in range(len(doc) - total):
                flag = 1
                for k in common:
                    if k not in doc[j:j + i]:
                        flag = 0
                        break
                if flag:
                    return [total / i, total / len(que)]

    def t_findall(self, que):
        # que = '交换的课程认定'  # '大二学天毕业论怎文的有多少人'#'教务处各科室的人要干嘛'#'胡金波觉得课程怎么样'
        que_cut = self.cut(que)
        que2 = self.cut2(que)
        text = self.ttf_idf(que2)
        text_cut = [x for x in map(self.cut, text)]

        v = CountVectorizer()
        t = TfidfTransformer()
        vv = v.fit_transform([que_cut] + text_cut)
        tt = t.fit_transform(vv[1:])
        qq = vv[0]
        r = tt.dot(qq.T)
        r = r / r.max()

        alpha = 1 / 8
        beta = 1
        lambda_ = 0.4

        res = []
        for i in range(len(text_cut)):
            res += [[i, self.f(text_cut[i], que_cut), r[i, 0]]]
            # res+=[[i,f(text[i],que)]]

        res = sorted(res, key=lambda x: lambda_ * x[2] + (1 - lambda_) * (x[1][0] ** alpha) * (x[1][1] ** beta),
                     reverse=True)
        # print(res)
        last_count = 0
        last_result = ""
        for i in range(len(res)):
            last_result = last_result + text[res[i][0]]
            # print(text[res[i][0]])
            last_count += 1
            # if (lambda_ * x[2] + (1 - lambda_) * (x[1][0] ** alpha) * (x[1][1] ** beta)) <= 0.45:
            #    break
            if last_count >= 8:
                break
        return last_result
        # print([lambda_ * x[2] + (1 - lambda_) * (x[1][0] ** alpha) * (x[1][1] ** beta) for x in res])

    def findall(self, que):
        # que = '交换的课程认定'  # '大二学天毕业论怎文的有多少人'#'教务处各科室的人要干嘛'#'胡金波觉得课程怎么样'
        que_cut = self.cut(que)
        que2 = self.cut2(que)
        text = self.ttf_idf(que2)
        text_cut = [x for x in map(self.cut, text)]

        v = CountVectorizer()
        t = TfidfTransformer()
        vv = v.fit_transform([que_cut] + text_cut)
        tt = t.fit_transform(vv[1:])
        qq = vv[0]
        r = tt.dot(qq.T)
        r = r / r.max()

        alpha = 1 / 8
        beta = 1
        lambda_ = 0.4

        res = []
        for i in range(len(text_cut)):
            res += [[i, self.f(text_cut[i], que_cut), r[i, 0]]]
            # res+=[[i,f(text[i],que)]]

        res = sorted(res, key=lambda x: lambda_ * x[2] + (1 - lambda_) * (x[1][0] ** alpha) * (x[1][1] ** beta),
                     reverse=True)
        # print(res)
        last_count = 0
        last_result = {}
        for i in range(len(res)):
            last_result[text[res[i][0]]] = self.return_dict[text[res[i][0]]]
            # print(text[res[i][0]])
            last_count += 1
            if last_count >= 10:
                break
        return last_result


if __name__ == '__main__':
    c = TermFreqInvDocFreq()
    print(c.findall('交换生的课程认定'))

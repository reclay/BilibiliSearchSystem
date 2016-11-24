# coding=utf8


import os
import codecs

import jieba
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.index import create_in, open_dir
from lxml import etree
from whoosh.qparser import QueryParser

XML_DIR = '../bizhan/xml_dir'
INDEX_DIR = 'index_dir'
DIC_DIR = 'dictionary'

AD_DIC = 'ad.txt'
POLITICS_DIC = 'politics.txt'
SALACITY_DIC = 'salacity.txt'
STOPWORD_DIC = 'stopword.dic'


def load_stop_word():
    stop_word_path = os.path.join(DIC_DIR, STOPWORD_DIC)
    stop_word = list()
    with codecs.open(stop_word_path, 'r', 'utf8') as f:
        for i in f.readlines():
            w = i.strip()
            if len(w) > 0:
                stop_word.append(w)
    return set(stop_word)


def load_ad_word():
    ad_word_path = os.path.join(DIC_DIR, AD_DIC)
    ad_word = list()
    with codecs.open(ad_word_path, 'r', 'utf8') as f:
        for i in f.readlines():
            w = i.strip()
            if len(w) > 0:
                ad_word.append(w)
    return set(ad_word)


def load_politics_word():
    politics_word_path = os.path.join(DIC_DIR, POLITICS_DIC)
    politics_word = list()
    with codecs.open(politics_word_path, 'r', 'utf8') as f:
        for i in f.readlines():
            w = i.strip()
            if len(w) > 0:
                politics_word.append(w)
    return set(politics_word)


def load_salacity_word():
    salacity_word_path = os.path.join(DIC_DIR, SALACITY_DIC)
    salacity_word = list()
    with codecs.open(salacity_word_path) as f:
        for i in f.readlines():
            w = i.strip()
            if len(w) > 0:
                salacity_word.append(w)
    return set(salacity_word)


def load_all_words():

    filter_words = set()
    ad_word = load_ad_word()
    filter_words = filter_words | ad_word

    salacity_word = load_salacity_word()
    filter_words = filter_words | salacity_word

    politics_word = load_politics_word()
    filter_words = filter_words | politics_word

    stop_word = load_stop_word()
    filter_words = filter_words | stop_word

    return filter_words


def index():

    '''
    对于弹幕信息进行检索，如果lxml解析报错，去掉该文件将不被检索
    '''
    
    f_list = os.listdir(XML_DIR)
    schema = Schema(path=ID(stored=True), content=TEXT(stored=True))

    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()

    filter_words = load_all_words()

    for fname in f_list:
        filename = os.path.join(XML_DIR, fname)
        with codecs.open(filename, 'r', 'utf8') as f:
            content = f.read()
            try:
                node = etree.XML(content.encode('utf8'))
                danmu_xpath = "//d/text()"
                text_list = []
                for danmu in node.xpath(danmu_xpath):
                    word_list = jieba.cut(danmu.strip())
                    sentence = " ".join([w for w in word_list if w not in filter_words and len(w.strip())>0])
                    if len(sentence) > 0:
                        text_list.append(sentence)
                if len(text_list)>0:
                    text_value = ' \n '.join(text_list)
                    writer.add_document(path=fname.decode('utf8'),
                                    content=text_value)
            except Exception, e:
                print filename
                print e
    writer.commit()


def query(query_phrase):
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    filter_words = load_all_words()
    word_list = jieba.cut(query_phrase)
    query_phrase = " ".join([w for w in word_list if w not in filter_words and len(w.strip())>0])
    query_phrase = query_phrase.replace("  "," ")
    
    print type(query_phrase),query_phrase

    ix = open_dir(INDEX_DIR)
    
    with ix.searcher() as searcher:

        query = QueryParser("content", ix.schema).parse(query_phrase)
        results = searcher.search(query, limit=50)
        print results
        for e in results[:5]:
            print e.highlights("content").encode('utf8')
            print "from", e["path"]
            print '*'*20
    ix.close()

if __name__ == '__main__':
    # index()
    query(u"撸")
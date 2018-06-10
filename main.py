from collections import OrderedDict
from functools import reduce

import classUtils
import codecs
import glob
import pickle
import pickle
import sys

def index(documents):
    listPosting = []
    posting_dict = dict()
    for document in documents:
        for word in document.words:
            if word in posting_dict:
                posting_dict[word].append(document.url)
            else:
                posting_dict[word] = [document.url]
    for key in posting_dict:
        listPosting.append(classUtils.Posting(key, posting_dict[key]))
    return listPosting

def build(postings):
    urlDict = dict()
    wordDict = dict()
    idx = 0
    for p in postings:
        for u in p.url:
            if u not in urlDict:
                urlDict[u] = idx
                idx += 1

    for p in postings:
        word = p.word
        for u in p.url:
            if (word in wordDict):
                wordDict[word].append(urlDict[u])
            else:
                wordDict[word] = [urlDict[u]]
    return classUtils.Index(urlDict, wordDict)

def save(index, path):
    file = open(path, 'wb')
    pickle.dump(index, file)
    file.close()

def fetch(path, recursive = True):
    documents = []
    files = glob.glob(path + '/**/**')
    for filename in files:
        with codecs.open(filename, 'r', 'utf-8', 'ignore') as text:
            doc = classUtils.Document(text.read(), filename)
            documents.append(doc)
    return documents

def analyze(documents, processors):
    words = documents.text.split()
    newWordList = []
    for word in words:
        word = processors.process(word)
        newWordList.append(word)
    tD = classUtils.TokenizedDocument(list(filter(None, newWordList)), documents.url)
    return tD

def load(path):
    file = open(path, "rb")
    index = pickle.load(file)
    file.close()
    return index

def search(index, word):
    word = word[0]
    listUrl = []
    if (word not in index.wordToDids):
        return []
    
    urlIds = index.wordToDids[word]
    urlIds = list(set(urlIds))

    for urlId in urlIds:
        for key in index.urlToDid:
            if (index.urlToDid[key] == urlId):
                listUrl.append(key)
    return listUrl

def searchAND(index, words):
    listUrl = []
    urlIds = []

    for word in words:
        urlIds.append(index.wordToDids[word])
    urlIds = list(reduce(set.intersection, map(set, urlIds)))

    for urlId in urlIds:
        for key in index.urlToDid:
            if index.urlToDid[key] == urlId:
                listUrl.append(key)

    return listUrl

def searchOR(index, words):
    listUrl = []
    for word in words:
        listUrl.append(search(index, word))
    return list(reduce(set.union, map(set, listUrl)))


if len ( sys.argv ) != 2:
    sys.stderr.write( "Usage: python main.py [ data folder ]" )
else:
    print("Fetching data in", sys.argv[1], "...")
    listDoc = fetch(sys.argv[1])
    listTd = []
    for doc in listDoc:
        td = analyze(doc, classUtils.Normalizer())
        listTd.append(td)
    p = index(listTd)
    print("Creating index ...")
    builded = build(p)
    save(builded, "data.bin")
    #index = load("data.bin")
    res = input("Which search do you want to perform ? (1. unique; 2. AND; 3. OR) ")
    w = input("Which word(s) do you want to search ? ").split()
    print("Searching the word", w, "...")
    if int(res) == 1:
        l = search(builded, w)
        opt = ""
    elif int(res) == 2:
        l = searchAND(builded, w)
        opt = "AND"
    elif int(res) == 3:
        l = searchOR(builded, w)
        opt = "OR"
    if (len(l) == 0):
        print("Nothing found :(")
    else:
        for li in l:
            print(li)
        print("\n" + str(len(l)), "results for the word", w, opt)

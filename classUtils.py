import re

class TokenizedDocument:
    def __init__(self, words, url):
        self.words = words
        self.url = url

class Normalizer:
    def process(self, word):
        lowerCase = word.lower()
        return re.sub('[^A-Za-z-0-9]+', '', lowerCase)

class Document:
    def __init__(self, text, url):
        self.text = text
        self.url = url

class Posting:
    def __init__(self, word, url):
        self.word = word
        self.url = url

class Index:
    def __init__(self, urlToDid, wordToDids):
        self.urlToDid = urlToDid
        self.wordToDids = wordToDids

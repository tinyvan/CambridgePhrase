# 此工具可以获取单词相关短语及释义! (数据来自剑桥词典)

from bs4 import BeautifulSoup
import requests
import lxml
cambridge_url = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/{0}'
cambridge_phrase_url = 'https://dictionary.cambridge.org/{0}'
firefox_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


class CambridgePhraseBook:
    word = ''
    phrases = {}

    def __init__(self, word: str):
        self.word = word
        word_request = requests.get(
            cambridge_url.format(word), headers=firefox_header)
        word_html = word_request.content
        word_html_analyzer = BeautifulSoup(word_html, 'lxml')
        phrases_list = word_html_analyzer.find_all(
            'div', class_='item lc lc1 lc-xs6-12 lpb-10 lpr-10')
        for phrase in phrases_list:
            self.phrases[phrase.text] = []
            phrase_request = requests.get(cambridge_phrase_url.format(
                phrase.a['href']), headers=firefox_header)
            phrase_html = phrase_request.content
            phrase_html_analyzer = BeautifulSoup(phrase_html, 'lxml')
            for meaning in phrase_html_analyzer.find_all("span", class_="trans dtrans dtrans-se break-cj"):
                self.phrases[phrase.text].append(meaning.text)
        pass

    def json(self):
        json_dict = {'word': self.word, 'phrases': self.phrases}
        return json_dict

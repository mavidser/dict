#!/usr/bin/python
          
from bs4 import BeautifulSoup
import requests
import threading
import json
import atexit
import sys

dictionary = {}

def main():
  with open('python_dict1.txt', 'r') as f:
    words_list = f.read()
  
  length = len(words_list.split())
  # langugages = ['hi', 'bn', 'gu', 'mr', 'pa', 'ta', 'te']
  langugages = ['hin', 'ben', 'gju', 'tel']
  lang_threads = {}


  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}



  def parse_dict(word,lang):
    dictionary[word][lang] = []
    url = 'https://glosbe.com/gapi/translate?from=eng&dest='+lang+'&format=json&phrase='+word+'&pretty=true'
    # url = 'http://www.shabdkosh.com/'+lang+'/translate?e='+word+'&l='+lang
    # try:
    # print 'Hier k\u0102\u015bnnen Sie sich kostenlos registrieren und / oder einloggen!'.decode('unicode-escape').encode('utf-8')
    html_doc = requests.get(url, headers=headers, timeout=5).json()
    # soup = BeautifulSoup(html_doc)
    try:
      for i in html_doc['tuc']:
        try:
          elem_text = i['phrase']['text']
          dictionary[word][lang].append(elem_text)
        except:
          pass
    except Exception as e:
      print e
      pass

    if len(dictionary[word][lang]) > 0:
      print >> sys.stderr, '.',
    else:
      print >> sys.stderr, word+':'+lang,

  for word in words_list.split():
    # print word
    word = word.lower()
    dictionary[word] = {}
    for lang in langugages:
      lang_threads[lang] = threading.Thread(target=parse_dict, args=(word,lang))
      lang_threads[lang].daemon = True
      lang_threads[lang].start()

      # print '',lang
    for lang in langugages:
      lang_threads[lang].join()

      
    # print json.dumps(dictionary, ensure_ascii=False, indent=2, sort_keys=True)
    # print 'w'

def exit_handler():
  print json.dumps(dictionary, ensure_ascii=False, indent=2, sort_keys=True)

atexit.register(exit_handler)

if __name__ == '__main__':
  main()

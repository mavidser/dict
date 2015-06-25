#!/usr/bin/python
          
from bs4 import BeautifulSoup
import time
import requests
import threading
import json
import atexit
import sys

dictionary = {}

def main():
  with open('english_python.txt', 'r') as f:
    words_list = f.read()
  
  length = len(words_list.split())
  # langugages = ['hi', 'bn', 'gu', 'mr', 'pa', 'ta', 'te']
  langugages = ['hi', 'bn', 'gu', 'te']
  lang_threads = {}


  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}



  def parse_dict(word,lang):
    dictionary[word][lang] = {}
    # url = 'https://glosbe.com/gapi/translate?from=eng&dest='+lang+'&format=json&phrase='+cat+'&pretty=true'
    url = 'http://www.shabdkosh.com/'+lang+'/translate?e='+word+'&l='+lang
    print >> sys.stderr, '.',
    # try:
    # print 'Hier k\u0102\u015bnnen Sie sich kostenlos registrieren und / oder einloggen!'.decode('unicode-escape').encode('utf-8')
    try:
      html_doc = requests.get(url, headers=headers, timeout=5).text
      soup = BeautifulSoup(html_doc)
      try:
        sections = soup.select('html > body > div#content > div#ehresults > div.row')[0].contents[0].contents[0].select('div.row')[0]
        for category in sections.contents:
          category_text = category.h3.get_text()
          # print ' ',category_text
          dictionary[word][lang][category_text] = []
          for elem in category.ol:
            elem_text = elem.a.get_text()
            # print '  ',elem_text
            dictionary[word][lang][category_text].append(elem_text)
        # except Exception as err:
        #   print 'Error on',word,lang
        #   print err
      except:
        print >> sys.stderr, word+':'+lang,
    except:
      print >> sys.stderr, word+'|'+lang,

  for word in words_list.split():
    # print word
    dictionary[word] = {}
    for lang in langugages:
      parse_dict(word,lang)
      # time.sleep(2)
    #   lang_threads[lang] = threading.Thread(target=parse_dict, args=(word,lang))
    #   lang_threads[lang].daemon = True
    #   lang_threads[lang].start()

    #   # print '',lang
    # for lang in langugages:
    #   lang_threads[lang].join()

      
    # print json.dumps(dictionary, ensure_ascii=False, indent=2, sort_keys=True)
    # print 'w'

def exit_handler():
  print json.dumps(dictionary, ensure_ascii=False, indent=2, sort_keys=True)

atexit.register(exit_handler)

if __name__ == '__main__':
  main()

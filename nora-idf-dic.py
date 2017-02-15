# coding: utf-8
from __future__ import print_function
import os
import sys
import re
import xml.etree.ElementTree as et
import MeCab
from collections import Counter 
import json
import math
import pickle
import plyvel

def wakati():
  db = plyvel.DB('title_context.ldb', create_if_missing=True)
  m = MeCab.Tagger ("-Owakati")
  cursol = None
  count  = 0
  for i, (event, elem) in enumerate(et.iterparse('./jawiki-20170201-pages-articles-multistream.xml')):
    # free memory
    if count%2500 == 0:
      print("now docs %d"%count)
    
    if 'title' in elem.tag:
      cursol = elem.text.replace('\n', '')
      continue
    if 'text' in elem.tag:
      count += 1
      if db.get(bytes(cursol, 'utf-8')) is not None: 
        continue
      if elem.text == None:
        continue
      text = elem.text.replace('\n', '')
      for remove in [re.compile(x, re.MULTILINE) for x in  [r'\(.*\)', r'\[\[', r'\]\]', r'<.*?>', r'\[.*?\]', r'{{.*?}}']]:
        text = re.sub(remove, '', text)
      parsed = m.parse(text)
      if parsed == None:
        continue
      db.put(bytes(cursol, 'utf-8'), pickle.dumps(parsed.split()) ) 
    elem.clear()
  print("total len=%d"%i)

def build_idf():
  db_source = plyvel.DB('title_context.ldb', create_if_missing=False)
  maxdocs = 1
  title_bow = {}
  words_freq = {}
  for title, serialized in db_source:
    maxdocs += 1
    context = pickle.loads(serialized)
    title_bow.update({ title:dict(Counter(context)) } )
    for word in set(context):
      if words_freq.get(word) is None: words_freq[word] = 0.
      words_freq[word] += 1.
    if maxdocs%10000 == 0:
      print("now loading... at %d"%maxdocs)
  print("total words len = %d"%len(words_freq)) 
  
  words_idf = {}
  for e, (word, freq) in enumerate(words_freq.items()):
    if e%1000 == 0:
      print("now evaluating... at %d/%d"%(e,len(words_freq)))
    weight = math.log( float(maxdocs) / freq )
    words_idf[word] = math.log( float(maxdocs) / freq ) 
  open('words_idf.json', 'w').write(json.dumps(words_idf)) 

def main():
  if '--wakati' in sys.argv:
    wakati()
  if '--build' in sys.argv:
    build_idf()
  if '-c' in sys.argv:
    idf = json.loads(open('words_idf.json').read())
    for w, idf in sorted(idf.items(), key=lambda x:x[1]):
      print(w, idf)

if __name__ == '__main__':
  main()

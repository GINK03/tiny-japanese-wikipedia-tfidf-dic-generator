import json
from collections import Counter
serval = "サーバル 　 ごめんね 、 あたし 、 かり ごっこ が だいすき で ！ 　 あなた 、 かり ごっこ が あんまり すき じゃ  ない けもの な ん だ ね 。".split()
tf = dict(Counter(serval))
idf = json.loads(open('words_idf.json').read())

tfidf =  {t:f*idf[t] for t,f in tf.items() } 

print( tfidf )

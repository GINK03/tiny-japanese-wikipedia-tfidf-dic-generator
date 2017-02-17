# nora(野良)-idf-dic

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

WikiepdiaのダンプファイルからIDF辞書を辞書を構築するスクリプトです。

  - LevelDB(kvs)を利用した省メモリ設計で、すべてのWikipediaのコンテンツコンテンツを取得可能
  - XGBoostやElasticNetなど他のアルゴリズムでの前処理に
  - JSONスキーマなので、Python以外の他のスクリプト言語でも利用可能
  
### プロジェクトの取得取得と、周辺ソフトウェアウェアのインストール
LevelDB(kvs)のインストール
(Ubuntu 16.04以上を想定しています)
```sh
$ git clone https://github.com/google/leveldb.git
$ cd leveldb
$ make 
$ cd include
$ sudo cp -r leveldb
$ sudo cp -r leveldb/ /usr/local/include/
$ cd ..
$ cd out-shared
$ sudo cp lib* /usr/local/lib/
$ sudo ldconfig
$ cd ~
```
mecabのインストール
```sh
$ sudo apt install mecab libmecab-dev mecab-ipadic
$ sudo apt install mecab-ipadic-utf8
```
mecab-python3, plyvelのインストール
```sh
$ git clone https://github.com/GINK03/tiny-japanese-wikipedia-tfidf-dic-generator
$ sudo pip3 install mecab-python3
$ sudo pip3 install plyvel
```
NeoLogdのインストール、及び辞書の書き換え
```
$ cd ~
$ git clone https://github.com/neologd/mecab-ipadic-neologd.git
$ cd mecab-ipadic-neologd/
$ ./bin/install-mecab-ipadic-neologd
[install-mecab-ipadic-NEologd] : Do you want to install mecab-ipadic-NEologd? Type yes or no.
>yes
$ sudo vi /etc/mecabrc
(元)dicdir = /var/lib/mecab/dic/debian -> (変更後)dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd
```
Neologdのテスト
```sh
$ echo "Fate/Grand Order" | mecab
Fate/Grand Order        名詞,固有名詞,一般,*,*,*,Fate/Grand Order,フェイトグランドオーダー,フェイトグランドオー ダー
EOS
```
動作確認
```sh
$ cd ~
$ cd tiny-japanese-wikipedia-tfidf-dic-generator
$ python3 nora-idf-dic.py
(何も表示されなけばOK)
```

### Wikipediaのダンプ情報の取得
Wikipediaのスナップショットと呼ばれる情報を取得し、展開します。
```sh
$ wget https://dumps.wikimedia.org/jawiki/20170201/jawiki-20170201-pages-articles-multistream.xml.bz2
$ bunzip2 jawiki-20170201-pages-articles-multistream.xml.bz2
```
idf辞書を構築します。
```sh
$ python3 nora-idf-dic.py --wakati
(...60分ほど待ちます)
$ ls 
title_context.ldb(このディレクトリがあればOK)
$ python3 nora-idf-dic.py --build
(...3分ほど待ちます)
$ ls words_idf.json
words_idf.jsonls
```
## tf-idfでベクトル化する
具体例を記しておきます。
```sh
$ echo "あなた狩りごっこがあまり好きじゃないけものなんだね"  | python3 nora-idf-dic.py --check
{'ね': 4.926646596986834, 'ない': 2.042401886218362, 'だ': 2.8119346405476735, 'が': 1.2142350698667934, 'じゃ': 6.054326132384362, 'あなた': 5.476151075317936, 'ごっこ': 8.627077870130083, 'ん': 3.364157726200682, '狩り': 7.11635016692977, '好き': 4.97306829447642, 'けもの': 9.584680272531994, 'あまり': 5.093448481495583, 'な': 1.6713533531785785}
```
keyを数値としてindexを振っていけば、libsvmやXGBoostやLightGBMで入力可能なフォーマットになります。


License
----

Text of Creative Commons Attribution-ShareAlike 3.0 Unported License


**Free Software, Hell Yeah!**

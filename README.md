# CoreNLP-Parsey-Server
CoreNLPのPostaggerの部分をParseyMcParsefaceに入れ替えたものです。

[Stanford Core NLP](https://github.com/stanfordnlp/CoreNLP)と[algo-hub/parsey-universal-server](https://github.com/algo-hub/parsey-universal-server)を合わせたものです。

## 使い方
### コンパイル等が必要ない場合
2018/05/30時点の[image](https://hub.docker.com/r/takuyakubo/core-parsey/)をuploadしてあるので、それを使う。

```
$ docker pull takuyakubo/core-parsey
$ docker run -it -p 5000:5000 -p 9000:9000 takuyakubo/core-parsey
```

### コンパイル等が必要な場合

1. CoreNLPの中で `ant jar`
2. CoreNLPの中に [ここ](https://stanfordnlp.github.io/CoreNLP/index.html#download)からmodelをdownloadする。(英語の場合は2つであることに注意)
3. repository topに戻り `docker build -t "core-parsey" .`
4. `docker run -it -p 5000:5000 -p 9000:9000 core-parsey`

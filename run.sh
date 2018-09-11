#!/bin/bash

cd /opt/tensorflow/syntaxnet/syntaxnet/models/parsey_universal

#start the first process
python /opt/tensorflow/syntaxnet/server.py &

cd /opt/corenlp

export CLASSPATH="$CLASSPATH:javanlp-core.jar:stanford-english-corenlp-2018-02-27-models.jar:stanford-english-kbp-corenlp-2018-02-27-models.jar";
for file in `find lib -name "*.jar"`; do export CLASSPATH="$CLASSPATH:`realpath $file`"; done

# Start the second process
java -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

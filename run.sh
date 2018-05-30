#!/bin/bash

cd /opt/tensorflow/syntaxnet/syntaxnet/models/parsey_universal

#start the first process
python /opt/tensorflow/syntaxnet/server.py &

cd /opt/corenlp

# Start the second process
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

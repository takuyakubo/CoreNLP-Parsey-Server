FROM tensorflow/syntaxnet

RUN pip install Flask

ADD ./parsey/server.py /opt/tensorflow/syntaxnet
ADD ./parsey/parser.py /opt/tensorflow/syntaxnet

ENV CNLPDIR=/opt/corenlp/

RUN mkdir -p $CNLPDIR \
    && cd $CNLPDIR

WORKDIR $CNLPDIR

ADD ./CoreNLP/*.jar $CNLPDIR

ENV APPDIR=/opt/app

RUN mkdir -p $APPDIR \
    && cd $APPDIR

WORKDIR $APPDIR

EXPOSE 5000
EXPOSE 9000

Add ./run.sh $APPDIR

RUN chmod +x ./run.sh

CMD ./run.sh

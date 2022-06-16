FROM docker-local.artifactory.uber.internal:5922/devexp/generic-ci-container:latest
# FROM docker-local.artifactory.uber.internal:5922/devexp/udj-go-base:latest

RUN apt-get update \
    && apt-get install -y wget

RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz \
    && tar xvf Python-3.6.3.tgz \ 
    && cd Python-3.6.3 \
    && ./configure --with-ensurepip=install --prefix=/work/.local \
    && make -j8 \
    && make altinstall

#RUN /work/.local/bin/pip3.6 install -i https://yoober11:xa8TahJooch6toot9p@pypi.uberinternal.com/index tm1cm
RUN /work/.local/bin/pip3.6 install -i https://yoober11:xa8TahJooch6toot9p@pypi.uberinternal.com/index tm1cm[taptools] --upgrade

RUN apt-get install -y netcat

RUN /work/.local/bin/pip3.6 install pylint

# ENTRYPOINT ["/build/run/entrypoint.sh"]
# CMD [ "./test.sh" ]

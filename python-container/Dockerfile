#use existing docker file
FROM alpine
#download and install
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
ADD sort.py ./sort.py
#RUN touch sk.py
#RUN echo "print('Running in docker container...')">>sk.py
#what to do
CMD ["/sort.py"]
ENTRYPOINT ["python3"]

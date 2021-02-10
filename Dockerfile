FROM python:3.9.1-slim-buster

# copy all the files from here into image /src/
COPY /src $HOME/src

ADD requirements.txt $HOME/

RUN pip3 install -r /requirements.txt

EXPOSE 5000
WORKDIR $HOME/src/
CMD ["python3", "/itu-minitwit/minitwit.py"]
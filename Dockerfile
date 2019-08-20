FROM python:3.7.3

ENV BERKELEYDB_DIR=/usr
RUN apt update && apt-get install -y libdb++-dev libhunspell-dev
RUN python3 -m pip install gutenberg
COPY populate_cache.py populate_cache.py
RUN python3 populate_cache.py
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
RUN python -m nltk.downloader punkt
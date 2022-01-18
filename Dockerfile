FROM ubuntu:latest

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update \
    && apt install -y htop python3-dev wget

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir root/.conda \
    && sh Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN conda create -y -n ml python=3.7


COPY DatenSammlung.py ./DatenSammlung.py
COPY DatenVerarbeitung.py ./DatenVerarbeitung.py
COPY Modellierung.py ./Modellierung.py
COPY requirements.txt ./requirements.txt


RUN /bin/bash -c "source activate ml \
    && pip install -r requirements.txt"

RUN python3 Modellierung.py
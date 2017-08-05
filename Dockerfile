FROM python:3.6

WORKDIR /app

COPY 01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install pandoc texlive-full -qy && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/cache/* && \
    rm -rf /var/tmp/* && \
    rm -rf /tmp/* && \
    rm -rf /root/.npm && \
    rm -rf /root/.cache

RUN mkdir -p /app

COPY /requirements /app/requirements

RUN pip install -r /app/requirements/base.txt

ENV FLASK_APP=pandoc_api.py

RUN groupadd -r pandoc && useradd -r -g pandoc pandoc

COPY . /app

CMD uwsgi --wsgi-file pandoc_api.py --http 0.0.0.0:5000 --callable app --threads 12 --uid=pandoc

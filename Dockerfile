FROM python:3.6

WORKDIR /app

RUN apt-get update -qy && apt-get upgrade -qy && \
    apt-get install pandoc texlive -qy && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/cache/* && rm -rf /var/tmp/* && rm -rf /tmp/* && \
    rm -rf /root/.npm && rm -rf /root/.cache

RUN mkdir -p /app

COPY /requirements /app/requirements

RUN pip install -r /app/requirements/base.txt

CMD uwsgi --wsgi-file pandoc_api.py --http 0.0.0.0:5000 --callable app --threads 12

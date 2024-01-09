FROM python:3.10

ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ./entrypoint.sh ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./entrypoint.sh"]
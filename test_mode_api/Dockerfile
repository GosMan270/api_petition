FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 7000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "7000"]
FROM python:3.14
RUN mkdir /Backend
WORKDIR /Backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python","main.py"]
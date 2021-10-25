FROM python:3.7.4

WORKDIR /BackEnd

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "app.py" ]
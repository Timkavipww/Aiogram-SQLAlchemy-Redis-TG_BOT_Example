FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]
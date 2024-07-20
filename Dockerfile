FROM python:3.10

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock* ./

RUN pipenv install --system

COPY src .

CMD ["python", "slack_app.py"]
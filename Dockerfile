FROM python:3.10

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock* ./

RUN pipenv install --system --deploy

COPY . .

CMD ["python", "src/slack_app.py"]
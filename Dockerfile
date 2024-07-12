FROM python:3.10

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock* ./

RUN pipenv install --system --deploy

COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
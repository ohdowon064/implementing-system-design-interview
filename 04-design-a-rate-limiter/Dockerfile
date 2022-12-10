FROM python:3.11-slim-buster as requirements-stage
WORKDIR /code
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11-slim-buster
WORKDIR /code
COPY . .

RUN apt-get update && apt-get install -y openbabel && rm -rf /var/lib/apt/lists/*

COPY --from=requirements-stage /code/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

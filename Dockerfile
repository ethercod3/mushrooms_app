FROM python

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

RUN poetry install

COPY . . 

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]
FROM python:3.8

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install "uvicorn[standard]"
ENV PYTHONPATH=.

COPY . /app

ENV PATH="/root/.local/bin:$PATH"

RUN poetry update

CMD ["poetry", "run", "python3", "data_tracker/__main__.py"]
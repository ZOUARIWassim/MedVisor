ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS requirements_stage
WORKDIR /code
RUN pip install --no-cache-dir poetry poetry-plugin-export
COPY pyproject.toml poetry.lock ./


FROM requirements_stage AS dev-stage
RUN bash -c "poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev"

FROM requirements_stage AS run-stage
RUN bash -c "poetry export -f requirements.txt --output requirements.txt --without-hashes "

FROM requirements_stage AS notebook-stage
RUN bash -c "poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev,notebook"

FROM requirements_stage AS vscode-stage
RUN bash -c "poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev"

FROM python:${PYTHON_VERSION}-slim AS base
WORKDIR /code
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools wheel
COPY --from=run-stage /code/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

FROM base AS dev
COPY --from=dev-stage /code/requirements.txt /code/requirements.dev.txt
RUN pip install --no-cache-dir -r /code/requirements.dev.txt
RUN pip install --no-cache-dir uvicorn
ENTRYPOINT ["./docker-entrypoint.sh"]

FROM base AS notebook
COPY --from=notebook-stage /code/requirements.txt /code/requirements.notebook.txt
RUN pip install --no-cache-dir -r /code/requirements.notebook.txt
COPY . .
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''"]

FROM base AS vscode
COPY --from=vscode-stage /code/requirements.txt /code/requirements.vs-code.txt
RUN pip install --no-cache-dir -r /code/requirements.vs-code.txt
COPY . .

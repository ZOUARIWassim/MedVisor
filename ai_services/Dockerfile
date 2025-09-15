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
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
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

FROM base AS mlflow
RUN mkdir -p /mlflow/artifacts && chmod -R 777 /mlflow
ENV MLFLOW_DEFAULT_ARTIFACT_ROOT=/mlflow/artifacts
COPY --from=run-stage /code/requirements.txt /code/requirements.mlflow.txt
RUN pip install --no-cache-dir -r /code/requirements.mlflow.txt
COPY . .
CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--backend-store-uri", "sqlite:////mlflow/mlflow.db", \
     "--default-artifact-root", "/mlflow/artifacts"]

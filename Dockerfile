# base stage
FROM python:3.10-slim AS base
USER root
SHELL ["/bin/bash", "-c"]

WORKDIR /resonant-soul

ARG NEED_MIRROR=1

RUN if [ "$NEED_MIRROR" == "1" ]; then \
        pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple && \
        pip3 config set global.trusted-host mirrors.aliyun.com; \
        mkdir -p /etc/uv && \
        echo "[[index]]" > /etc/uv/uv.toml && \
        echo 'url = "https://mirrors.aliyun.com/pypi/simple"' >> /etc/uv/uv.toml && \
        echo "default = true" >> /etc/uv/uv.toml; \
    fi; \
    pip3 install uv

ENV PATH=/root/.local/bin:$PATH

# builder stage
FROM base AS builder
USER root

WORKDIR /resonant-soul

# install dependencies from uv.lock file
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,id=ragflow_uv,target=/root/.cache/uv,sharing=locked \
    sed -i 's|mirrors.aliyun.com/pypi|pypi.org|g' uv.lock; \
    uv sync --python 3.10 --frozen --all-extras;


# production stage
FROM base AS production
USER root

WORKDIR /resonant-soul

# Copy Python environment and packages
ENV VIRTUAL_ENV=/resonant-soul/.venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENV PYTHONPATH=/resonant-soul/

COPY api api
COPY conf conf
COPY pyproject.toml uv.lock ./
COPY app.py ./

COPY docker/entrypoint.sh ./
RUN chmod +x ./entrypoint*.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
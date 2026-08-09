ARG CI_PROJECT_URL=''
ARG CI_COMMIT_SHA=''
ARG CI_COMMIT_TAG=''

ARG ALPINE_VERSION=3.20
ARG NGINX_VERSION=1.27.2-r1
ARG PYTHON_VERSION=3.11.10

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS build


RUN pip --disable-pip-version-check list --outdated --format=json | \
    python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | \
    xargs -n1 pip install --upgrade;

RUN apk add --update \
        bash \
        git \
        gcc \
        cmake \
        libc-dev \
        alpine-sdk \
        libffi-dev \
        build-base \
        curl-dev \
        libxml2-dev \
        gettext \
        pkgconf \
        postgresql16-dev \
        postgresql16-client \
        libpq-dev \
        # NginX: to download items
        openssl \
        curl \
        ca-certificates

RUN printf "%s%s%s%s\n" \
  "@nginx " \
  "http://nginx.org/packages/mainline/alpine/v" \
  `egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release` \
  "/main" \
  | tee -a /etc/apk/repositories

RUN curl -o /tmp/nginx_signing.rsa.pub https://nginx.org/keys/nginx_signing.rsa.pub; \
  openssl rsa -pubin -in /tmp/nginx_signing.rsa.pub -text -noout;
  
RUN pip install --upgrade \
    setuptools \
    wheel \
    setuptools-rust \
    twine

RUN mkdir -p /tmp/python_modules /tmp/python_builds


COPY dist/ /tmp/python_builds


RUN \
    pip download \
        --dest /tmp/python_modules \
        "$(ls /tmp/python_builds/centurion_erp-*-py3-none-any.whl)[docker]";


RUN cd /tmp/python_modules \
  # && export PATH=$PATH:~/.cargo/bin \
  && echo "[DEBUG] PATH=$PATH" \
  && ls -l; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.whl; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.tar.gz || true;



FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS prepare


ARG NGINX_VERSION

ENV CENTURION_STATIC_ROOT=/data/static
ENV PYTHONTZPATH=""


COPY requirements.txt requirements.txt

COPY requirements_dev.txt requirements_dev.txt

COPY --from=build /etc/apk/repositories /etc/apk/repositories

COPY --from=build /tmp/nginx_signing.rsa.pub /etc/apk/keys/nginx_signing.rsa.pub

COPY includes/ /

COPY --from=build /tmp/python_builds /tmp/python_builds 

COPY --from=build /var/cache/apk /var/cache/apk

COPY --from=build /root/.cache/pip /root/.cache/pip

# Install / Update packages
RUN pip --disable-pip-version-check list --outdated --format=json | \
        python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | \
        xargs -n1 pip install  \
            --no-cache-dir \
            --upgrade; \
    apk update; \
    apk upgrade; \
    apk add \
        nginx@nginx=${NGINX_VERSION} \
        postgresql16-client \
        libxml2; \
    pip install \
        --no-cache-dir \
        --no-index \
        --find-links /tmp/python_builds \
        centurion_erp[docker]; \
    chmod +x /entrypoint.sh; \
    export

# Setup nginx
RUN rm -rf /tmp/python_builds; \
    rm /etc/nginx/sites-enabled; \
    rm /etc/nginx/conf.d/default.conf; \
    mv /etc/nginx/conf.d/centurion.conf /etc/nginx/conf.d/default.conf;

# Check for nginx errors. (will fail if so)
RUN nginx -t;

# sanity check, https://github.com/nofusscomputing/centurion_erp/pull/370
RUN if [ ! $(python -m django --version) ]; then \
        echo "Django not Installed"; \
        exit 1; \
    fi;


ENV DJANGO_SETTINGS_MODULE=centurion_erp.centurion.settings


# Generate static content
RUN manage collectstatic --noinput;

# Remove packages not required.
RUN apk del --no-interactive \
        perl;

# Setup SupervisorD conf dir
RUN mkdir -p /etc/supervisor/conf.d;

# Remove Python Packages not required
RUN pip uninstall -y \
    setuptools \
    wheel;



FROM scratch


LABEL \
  org.opencontainers.image.vendor="No Fuss Computing" \
  org.opencontainers.image.title="Centurion ERP" \
  org.opencontainers.image.description="An ERP with a focus on ITSM and automation" \
  io.artifacthub.package.license="AGPL-3.0-only"


ARG CI_PROJECT_URL
ARG CI_COMMIT_SHA
ARG CI_COMMIT_TAG


ENV CENTURION_STATIC_ROOT=/data/static
ENV CI_PROJECT_URL=${CI_PROJECT_URL}
ENV CI_COMMIT_SHA=${CI_COMMIT_SHA}
ENV CI_COMMIT_TAG=${CI_COMMIT_TAG}
ENV PYTHONTZPATH=""

# Var must exist, even empty so that the metrics settings logic functions
# correctly
ENV PROMETHEUS_MULTIPROC_DIR="/data/prometheus"

# Prevent python depreciation warnings
ENV PYTHONWARNINGS=ignore

ENV IS_WORKER=False

ENV DJANGO_SETTINGS_MODULE=centurion_erp.centurion.settings


COPY \
    --from=prepare \
    --exclude=root/.cache/*/* \
    --exclude=var/cache/*/* \
    / /

WORKDIR /data


# In future, adjust port to 80 as nginX is now used (Will be breaking change)
EXPOSE 8000


VOLUME [ "/data", "/etc/itsm" ]


HEALTHCHECK --interval=10s --timeout=30s --start-period=30s --retries=3 CMD \
  supervisorctl status || exit 1


ENTRYPOINT ["/entrypoint.sh"]

---
title: Installation
description: Installation documentation for Centurion ERP by No Fuss Computing
date: 2024-07-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Centurion ERP is a simple application to deploy with the only additional requirements being that you have already deployed a database server and a RabbitMQ server. Centurion ERP is container based and is deployable via Docker or upon Kubernetes. Our images are available on [Docker Hub](https://hub.docker.com/r/nofusscomputing/centurion-erp).

Deployment of Centurion ERP is recommended to be behind a reverse proxy. This is required as the method used to setup the containers does not include any SSL setup. Due to this the reverse proxy will be required to conduct the SSL termination.

!!! note "TL;DR"
    `docker pull nofusscomputing/centurion-erp:latest`.


## Deploying Centurion

Centurion ERP is a container base application. You can deploy it with any container engine, like Docker and Kubernetes. Although its design is for kubernetes, you dont require a cluster to deploy it. With K3s you can deploy a [single node (single machine) with Kubernetes](../../ansible/collection/kubernetes/index.md) and deploy Centurion ERP upon it. This option provides the opportunity to quickly extend the size of the cluster should you require it.

Basic installation steps are as follows:

1. Deploy a Database Server

1. Deploy a RabbitMQ Server

1. Deploy a API container for Centurion ERP

1. Deploy a UI container for Centurion ERP

1. Deploy a Worker container for Centurion ERP

1. Deploy a reverse proxy _(Nginx / Apache, or any other proxy capable of being a HTTPS reverse proxy)_

1. Add settings file to path `/etc/itsm/settings.py` for both API and worker Centurion ERP containers.

1. Run migrations

    - Docker `docker exec -ti <container name or id> -- python manage.py migrate`

    - Kubernetes `kubectl exec -ti -n <namespace> deploy/<deployment-name> -- python manage.py migrate`

Deploying Centurion ERP is intended to be done behind a reverse proxy that conducts the TLS termination. This is by design and due to the following reasons:

- gunicorn has been setup to serve Centurion ERP via a websocket within the API container. The local Nginx installation proxies directly to this.

- Proxy headers have been setup to pass on the required information to gunicorn so that Centurion ERP functions correctly.

- The API container does not serve HTTP/443 (TLS), only HTTP/80 (insecure http).

- No sanitization of HTTP headers is done. The headers passed to the API container are considered and expected to be trusted.

With the above in mind there your reverse proxy must be setup with the following:

- required headers set by proxy are: `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Real-IP`.

- your proxy sanitizes any additional `X-Forwarded-*` headers

- Proxy setup to serve Centurion URL over HTTPS (TLS)

!!! danger "Proxy Headers"
    Failing to sanitize proxy headers, especially `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Real-IP` has the potential for your deployment to be compromised. As the setup of the reverse proxy is outside of the scope of this documentation, you should refer to the documentation of the proxy you are implementing.


## Centurion Components

Centurion ERP is not a monolithic application. ALL components have been broken into smaller modules so they can be scaled to meet demands as required. The components that make up a Centurion ERP deploymnent are:

- Database server

- RabbitMQ Server

- API

- Worker

- UI


### Database Server

As Centurion ERP is uses the Django Framework, Theoretically Every Django supported database is available. The reality is however, that we have only used PostgreSQL Server with Centurion ERP. By default if no database is configured a SQLite database will be used. This allows [tests](../development/testing.md) to function and to quickly spin up a deployment for testing.


### RabbitMQ Server

Centurion ERP uses RabbitMQ for its worker queue. As tasks are created when using Centurion ERP, they are added to the RabbitMQ server for the background worker to pickup. When the background worker picks up the task, it does it's business, clears the task from the RabbitMQ server and saves the [results](../user/core/index.md#background-worker) within the Database.


### API Container

The [API container](https://hub.docker.com/r/nofusscomputing/centurion-erp) is the guts of Centurion ERP. It provides the endpoints for interacting with Centurion ERP. This container is scalable with the only additional requirement being that a load-balancer be placed in front of all web containers for traffic routing. If deploying to Kubernetes the service load-balancer is sufficient and setting the deployment `replicas` to the number of desired containers is the simplest method to scale.

When setting up the reverse proxy, this container requires the following paths be passed to it:

- `/account/` - Account pages.

- `/admin/` - The Admin pages

- `/api/` - API Pages

- `/sso/` Single Sing on endpoint. This path is optional and only required if you have configured the Authentication to use an SSO service.

- `/static/` - Static assets used by Centurion ERP. i.e. styles, images etc.


### UI Container

!!! info
    Currently we are still developing the UI. As such it's still considered beta. This will remain until the new UI has [feature parity](https://github.com/nofusscomputing/centurion_erp_ui/issues/18) with the current django UI.

The [UI container](https://hub.docker.com/r/nofusscomputing/centurion-erp-ui) is the user interface for Centurion. The user interface uses the react framework so as to take advantage of the UI running locally on the users machine. This reduces the bandwidth requirements for using Centurion to be approximatly the data they request and not the page as well.

This container requires that the reverse proxy be setup to path the following path(s):

- `/` - The root path for Centurion ERP. Contains the React Application that is the entire UI


### Background Worker Container

The [Background Worker container](https://hub.docker.com/r/nofusscomputing/centurion-erp) is a worker that waits for tasks sent to the RabbitMQ server. The worker is based upon [Celery](https://docs.celeryq.dev/en/stable/index.html). On the worker not being busy, it'll pickup and run the task. This container is scalable with nil additional requirements for launching additional workers. If deploying to Kubernetes the setting the deployment `replicas` to the number of desired containers is the simplest method to scale. There is no container start command, however you will need to set environmental variable `IS_WORKER` to value `'True'` within the container.

Configuration for the worker resides in directory `/etc/itsm/` within the container. see below for the `CELERY_` configuration.

This container does not require any paths be passed to it from the reverse proxy.


## Settings file

The settings file is a python file `.py` and must remain a valid python file for the application to work. Settings for the application are stored within a docker volume at path `/etc/itsm/`, with the settings living in `.py` files. A database is also required for the application to store it's settings. PostgreSQL is supported.

``` py title="settings.py"

--8<-- "includes/etc/itsm/settings.py"

```


## Migrations

Migrations serve the purpose of setting up the database. On initial deployment of Centurion ERP migrations must be run as must they be on any upgrade.


## Updating

We use [semver](https://semver.org/) versioning for Centurion ERP. Using this method of versioning enables us to clearly show what versions will have breaking changes. You can rest assured that every version whose `Major` version number remains the same will not break your deployment. [Release notes](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/blob/master/Release-Notes.md) are available within the repository root and are a running document for the current `Major` release. To locate the release notes for your particular version please select the release tag from the branches drop-down. We will use the release notes to denote **Any** Breaking changes.

Updating to a newer version of Centurion ERP is as simple as [backing up your database](./backup.md) and RabbitMQ server, then updating the deployed image to the desired version and running the database migrations.

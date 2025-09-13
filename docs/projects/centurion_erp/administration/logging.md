---
title: Logging
description: Logging documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Centurion ERP has logging built. Logging within Centurion ERP creates its log files within `/var/log`


## Tracing

In addition and to assist with debugging code on a production system, Centurion ERP has trace debugging. This logging in particular logs the function/method calls along with assosiated variables, timings and calling information. This information can then be used by anyone to follow the complete executed code path for the full request cycle. If you must enable trace logging add `TRACE_LOGGING = True` to your settings and restart the Centurin ERP instance.

There are different levels of logging, to set, add `CENTURION_LOGGING['loggers']['centurion.trace']['level'] = CenturionLogger.<LEVEL>` to your settings file. Available values are:

- `INFO` Default Logs request, call start, call finish and viewset

- `DEBUG` Logs line calls within a function/method

- `TRACE` Logs all database queries

Normally you wont need to adjust this setting unless you want significantly more details within your logging.

!!! danger
    You are encouraged not to turn this on unless you require the details to debug the Centurion ERP code. When trace logging is enabled Centurion slows down considerably. This is because every call is recorded and subsequently logged. To bring this into perspective there can be in excess of 10,000 log lines created per http request. This is only amplified by the UI as it makes multiple requests on the users behalf every time the navigate between Centurion pages.

!!! danger
    By design, when trace logging is enabled information that may be considered sensitive will be logged. As such care should be taken with the log files to ensure that you dont inadvertantly share this information with anyone who should not have access.

!!! tip
    When enabling trace logging, if you remain logged into the server console, make the request to the problem page. as soon as the request is finished, immediatly disable trace logging (just remove `TRACE_LOGGING = True` from settings and restart the Centurin ERP instance)

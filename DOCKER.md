Running `temper.py` as a service in docker container
====================================================
*The container provides the sensor metrics via web API*

* Default port: `2610`
* endpoint `/list`: List available USB devices in JSON format
* endpoint `/metrics`: Send metrics from available temper devices in JSON format

Running the service as a commandline
------------------------------------
```sh
docker run --rm -it -p 2610:2610 temper/service:latest
```


Snippet of config in `docker-compose.yml`
-----------------------------------------
```yml
---
services:
  temper-py:
    container_name: temper-service
    image: temper/service:latest
    volumes:
      - /dev:/dev
    restart: unless-stopped
    pull_policy: build
    build:
      context: .
      dockerfile: temper-service.Dockerfile
      args:
        - --no-cache
    healthcheck:
      test: curl --fail http://localhost:2610/metrics || exit 1
      interval: 60s
      timeout: 30s
      retries: 3
      start_period: 10s
    ports:
      - 2610:2610
    privileged: true
```

Running the docker as a service using docker-compose config.
```sh
docker-compose up -d
```


Checking the service from another terminal
------------------------------------------
```sh
# List available USB devices (including temper devices)
http localhost:2610/list | jq -C

# Query temper metrics
http localhost:2610/metrics | jq -C 
```


Running the script `temper.py` from docker container
----------------------------------------------------
You can run `temper.py` as a docker container by overriding the entrypoint.
```
docker run --rm -it --entrypoint /opt/temper/bin/temper.py temper/service:latest --help
usage: temper.py [-h] [-l] [--json] [--force VENDOR_ID:PRODUCT_ID] [--verbose]

temper

options:
  -h, --help            show this help message and exit
  -l, --list            List all USB devices
  --json                Provide output as JSON
  --force VENDOR_ID:PRODUCT_ID
                        Force the use of the hex id; ignore other ids
  --verbose             Output binary data from thermometer
```

**Note:** This dockerization effort was sponsored by [Greenfly SAU LLC.][0]

[0]: https://greenfly.io

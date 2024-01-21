# Cold Person

## Install
If you don't have opinions then

```shell
make .venv
. .venv/bin/activate
make install
```

And then it should be possible to run tests with

```shell
make test
```

## Running
After having done an editable pip install (`make install`), just run
```
coldperson-serve
```

<details>
<summary>A cold person running on port 8080</summary>

```
~/src/python/pact-sweater-shop-python/cold-person (master) % coldperson-serve 
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

</details>

You can test the service with curl

```shell
curl '0.0.0.0:8080/healthz'
curl -H 'Content-Type: application/json' -d '{"colour":"white","order_number":1000}' '0.0.0.0:8080/bff/order'
```

The second might fail if upstream dependencies have not been started... ;)

See [../knitter](../knitter) and [../farmer](../farmer).

The services can be configured with environment variables
`PORT` can be use to configure an alternative port to listen on
`KNITTER_BASE_URL`, defaulting to `http://localhost:8081` can be configured
if you run `knitter` on a different port / address


### Running a stub Knitter

If we want to, we can use our pacts to run a stub service instead of
running the real knitter

```
docker pull pactfoundation/pact-stub-server
docker run -it --rm -p 8081:8081 -v "$PWD/pacts/:/app/pacts" pactfoundation/pact-stub-server -p 8081 -d pacts

# Test your stub endpoints
curl -H 'Content-Type: application/json' -d '{"colour":"white","order_number":28}' '0.0.0.0:8080/bff/order'
```



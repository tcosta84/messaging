# Messaging

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

Messaging is a microservice that let your application send short messages (SMS).

You can:
  - Set an expiration date so that your users do not receive outdated and irrelevant content;

You can't:
  - Send messages larger than 160 chars;

### Installation

Messaging requires [Python](https://python.org/) v3.5+ to run.

Install the dependencies, create database and start the server.

```sh
$ cd messaging
$ pip install -r requirements.txt
$ python manage.py db upgrade
$ python manage.py runserver
```

### API Documentation

Schema:

    {
        "type": "object",
        "properties": {
            "sender": {}
        }
    }

Method: PUT

Headers:
    - Content-type: application/json

Request example:

    {
        "sender": "21981527318",
        "receiver": "980072800",
        "body": "Hello!",
        "expiration_date": "2016-10-25T15:00"
    }

Respomse Status Code: 201 CREATED

Response example:

    {
        "detail": "Message sent."
    }

Sample call:

  ```shell
  curl -X PUT -H "Content-type: application/json" -d '{"from": "21981527318", "to": "21980072800", "body": "Hello!"}' -i http://localhost:5000/api/v1/send_sms
  ```

### Docker
Messaging is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 5000, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
cd messaging-service
npm run-script build-docker
```
This will create the dillinger image and pull in the necessary dependencies. Moreover, this uses a _hack_ to get a more optimized `npm` build by copying the dependencies over and only installing when the `package.json` itself has changed.  Look inside the `package.json` and the `Dockerfile` for more details on how this works.

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 8000 of the host to port 80 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart="always" <youruser>/dillinger:latest
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:5000
